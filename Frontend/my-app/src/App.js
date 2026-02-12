import React, { useState, useEffect } from 'react';
import { useReactMediaRecorder } from "react-media-recorder-2";
import axios from 'axios';
import { Mic, StopCircle, Tag, Send, ClipboardList } from 'lucide-react';

const ScrumRecorder = () => {
  const [segments, setSegments] = useState([]); // [{part: 'Backend', time: '01:20'}]
  const [logs, setLogs] = useState(["대기 중..."]);
  const [template, setTemplate] = useState("어제 한 일 / 오늘 할 일 / 이슈 사항");

  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true });

  // 로그 추가 함수
  const addLog = (msg) => setLogs(prev => [...prev, `[${new Date().toLocaleTimeString()}] ${msg}`]);

  // 파트 마커 기록 (현재 녹음 시간 기록)
  const markSegment = (part) => {
    if (status !== "recording") return;
    const now = new Date(); // 실제로는 녹음 시작 시점과의 차이를 계산해야 함
    setSegments([...segments, { part, time: now.toLocaleTimeString() }]);
    addLog(`${part} 파트 시작 지점 마킹 완료`);
  };

  // 백엔드로 데이터 전송
  const handleSubmit = async () => {
    if (!mediaBlobUrl) return;
    addLog("백엔드로 오디오 전송 시작...");

    const audioBlob = await fetch(mediaBlobUrl).then(r => r.blob());
    const formData = new FormData();
    formData.append("file", audioBlob, "scrum_audio.wav");
    formData.append("template", template);
    formData.append("segments", JSON.stringify(segments));

    try {
      const response = await axios.post("http://localhost:8000/api/v1/scrum", formData);
      addLog("전사 및 요약 완료!");
      console.log(response.data);
    } catch (error) {
      addLog("에러 발생: " + error.message);
    }
  };

  return (
    <div className="p-8 max-w-2xl mx-auto space-y-6">
      <h1 className="text-2xl font-bold flex items-center gap-2">
        <ClipboardList /> Scrum-Cutter Control Panel
      </h1>

      {/* 녹음 컨트롤 */}
      <div className="bg-gray-100 p-6 rounded-xl flex justify-around items-center">
        <button onClick={startRecording} className="flex flex-col items-center text-blue-600">
          <Mic size={48} /> <span>시작</span>
        </button>
        <div className="text-xl font-mono">{status}</div>
        <button onClick={stopRecording} className="flex flex-col items-center text-red-600">
          <StopCircle size={48} /> <span>정지</span>
        </button>
      </div>

      {/* 파트 마커 버튼 */}
      <div className="grid grid-cols-3 gap-4">
        {['Backend', 'Frontend', 'DevOps'].map(part => (
          <button 
            key={part}
            onClick={() => markSegment(part)}
            className="bg-white border-2 border-gray-200 p-3 rounded-lg hover:bg-gray-50 flex items-center justify-center gap-2"
          >
            <Tag size={16} /> {part}
          </button>
        ))}
      </div>

      {/* 상태 로그 창 */}
      <div className="bg-black text-green-400 p-4 rounded-lg h-40 overflow-y-auto font-mono text-sm">
        {logs.map((log, i) => <div key={i}>{log}</div>)}
      </div>

      <button 
        onClick={handleSubmit}
        disabled={!mediaBlobUrl || status === "recording"}
        className="w-full bg-blue-600 text-white py-3 rounded-xl font-bold flex items-center justify-center gap-2 disabled:bg-gray-400"
      >
        <Send size={20} /> 분석 및 노션 전송
      </button>
    </div>
  );
};

export default ScrumRecorder;