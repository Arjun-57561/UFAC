"use client";

import { useCallback } from "react";
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  addEdge,
  useNodesState,
  useEdgesState,
  type Connection,
  type Edge,
  type Node,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import { PageTransition } from "@/components/PageTransition";
import { motion } from "framer-motion";

const initialNodes: Node[] = [
  {
    id: "input",
    type: "default",
    position: { x: 50, y: 200 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">📥</div>
          <div className="font-bold">User Input</div>
          <div className="text-xs text-gray-500 mt-1">
            Farmer eligibility data
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
      color: "white",
      border: "2px solid #667eea",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(102, 126, 234, 0.3)",
    },
  },
  {
    id: "fact",
    type: "default",
    position: { x: 300, y: 50 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">🔍</div>
          <div className="font-bold">Fact Agent</div>
          <div className="text-xs text-gray-500 mt-1">
            Extracts confirmed facts
          </div>
          <div className="mt-2 px-2 py-1 bg-white/20 rounded text-xs">
            3 LLM runs
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
      color: "white",
      border: "2px solid #11998e",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(17, 153, 142, 0.3)",
    },
  },
  {
    id: "assumption",
    type: "default",
    position: { x: 300, y: 200 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">💭</div>
          <div className="font-bold">Assumption Agent</div>
          <div className="text-xs text-gray-500 mt-1">
            Identifies assumptions
          </div>
          <div className="mt-2 px-2 py-1 bg-white/20 rounded text-xs">
            3 LLM runs
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
      color: "white",
      border: "2px solid #f093fb",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(240, 147, 251, 0.3)",
    },
  },
  {
    id: "unknown",
    type: "default",
    position: { x: 300, y: 350 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">❓</div>
          <div className="font-bold">Unknown Agent</div>
          <div className="text-xs text-gray-500 mt-1">
            Detects missing info
          </div>
          <div className="mt-2 px-2 py-1 bg-white/20 rounded text-xs">
            3 LLM runs
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #fa709a 0%, #fee140 100%)",
      color: "white",
      border: "2px solid #fa709a",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(250, 112, 154, 0.3)",
    },
  },
  {
    id: "confidence",
    type: "default",
    position: { x: 550, y: 125 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">📊</div>
          <div className="font-bold">Confidence Agent</div>
          <div className="text-xs text-gray-500 mt-1">
            Calculates confidence
          </div>
          <div className="mt-2 px-2 py-1 bg-white/20 rounded text-xs">
            3 LLM runs
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
      color: "white",
      border: "2px solid #4facfe",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(79, 172, 254, 0.3)",
    },
  },
  {
    id: "decision",
    type: "default",
    position: { x: 550, y: 275 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">🎯</div>
          <div className="font-bold">Decision Agent</div>
          <div className="text-xs text-gray-500 mt-1">
            Generates next steps
          </div>
          <div className="mt-2 px-2 py-1 bg-white/20 rounded text-xs">
            3 LLM runs
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)",
      color: "#333",
      border: "2px solid #a8edea",
      borderRadius: "16px",
      width: 180,
      boxShadow: "0 4px 20px rgba(168, 237, 234, 0.3)",
    },
  },
  {
    id: "output",
    type: "default",
    position: { x: 800, y: 200 },
    data: {
      label: (
        <div className="text-center p-4">
          <div className="text-2xl mb-2">✅</div>
          <div className="font-bold text-lg">UFAC Response</div>
          <div className="text-xs text-gray-500 mt-1">
            Complete assessment
          </div>
        </div>
      ),
    },
    style: {
      background: "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
      color: "white",
      border: "3px solid #11998e",
      borderRadius: "16px",
      width: 200,
      boxShadow: "0 8px 30px rgba(17, 153, 142, 0.5)",
    },
  },
];

const initialEdges: Edge[] = [
  {
    id: "input-fact",
    source: "input",
    target: "fact",
    animated: true,
    style: { stroke: "#11998e", strokeWidth: 2 },
  },
  {
    id: "input-assumption",
    source: "input",
    target: "assumption",
    animated: true,
    style: { stroke: "#f093fb", strokeWidth: 2 },
  },
  {
    id: "input-unknown",
    source: "input",
    target: "unknown",
    animated: true,
    style: { stroke: "#fa709a", strokeWidth: 2 },
  },
  {
    id: "fact-confidence",
    source: "fact",
    target: "confidence",
    animated: true,
    style: { stroke: "#4facfe", strokeWidth: 2 },
  },
  {
    id: "assumption-confidence",
    source: "assumption",
    target: "confidence",
    animated: true,
    style: { stroke: "#4facfe", strokeWidth: 2 },
  },
  {
    id: "unknown-confidence",
    source: "unknown",
    target: "confidence",
    animated: true,
    style: { stroke: "#4facfe", strokeWidth: 2 },
  },
  {
    id: "fact-decision",
    source: "fact",
    target: "decision",
    animated: true,
    style: { stroke: "#a8edea", strokeWidth: 2 },
  },
  {
    id: "assumption-decision",
    source: "assumption",
    target: "decision",
    animated: true,
    style: { stroke: "#a8edea", strokeWidth: 2 },
  },
  {
    id: "unknown-decision",
    source: "unknown",
    target: "decision",
    animated: true,
    style: { stroke: "#a8edea", strokeWidth: 2 },
  },
  {
    id: "confidence-output",
    source: "confidence",
    target: "output",
    animated: true,
    style: { stroke: "#11998e", strokeWidth: 3 },
  },
  {
    id: "decision-output",
    source: "decision",
    target: "output",
    animated: true,
    style: { stroke: "#11998e", strokeWidth: 3 },
  },
];

export default function FlowPage() {
  const [nodes, , onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <PageTransition>
      <div className="h-[calc(100vh-4rem)]">
        {/* Header */}
        <div className="absolute top-4 left-1/2 -translate-x-1/2 z-10 bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] rounded-lg px-6 py-3 shadow-lg">
          <h1 className="text-2xl font-bold text-[hsl(var(--text-primary))]">
            UFAC Agent Flow
          </h1>
          <p className="text-sm text-[hsl(var(--text-muted))]">
            5-Agent Multi-LLM Architecture
          </p>
        </div>

        {/* React Flow */}
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          fitView
          className="bg-[hsl(var(--bg-primary))]"
        >
          <Background color="hsl(var(--border))" gap={16} />
          <Controls className="bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] rounded-lg" />
          <MiniMap
            className="bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] rounded-lg"
            nodeColor={(node) => {
              if (node.id === "input") return "#667eea";
              if (node.id === "fact") return "#11998e";
              if (node.id === "assumption") return "#f093fb";
              if (node.id === "unknown") return "#fa709a";
              if (node.id === "confidence") return "#4facfe";
              if (node.id === "decision") return "#a8edea";
              return "#11998e";
            }}
          />
        </ReactFlow>

        {/* Legend */}
        <div className="absolute bottom-4 left-4 bg-[hsl(var(--bg-card))] border border-[hsl(var(--border))] rounded-lg p-4 shadow-lg max-w-xs">
          <h3 className="font-semibold text-[hsl(var(--text-primary))] mb-2">
            Execution Flow
          </h3>
          <div className="space-y-2 text-sm text-[hsl(var(--text-secondary))]">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-[#667eea] to-[#764ba2]" />
              <span>User submits data</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-[#11998e] to-[#38ef7d]" />
              <span>Batch 1: Fact, Assumption, Unknown (parallel)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-[#4facfe] to-[#00f2fe]" />
              <span>Batch 2: Confidence, Decision (parallel)</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-gradient-to-r from-[#11998e] to-[#38ef7d]" />
              <span>Final UFAC response</span>
            </div>
          </div>
        </div>
      </div>
    </PageTransition>
  );
}
