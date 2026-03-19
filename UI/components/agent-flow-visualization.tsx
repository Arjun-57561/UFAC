'use client';

import { useCallback, useState, useEffect } from 'react';
import {
  ReactFlow,
  Node,
  Edge,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  ConnectionMode,
  Handle,
  Position,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { motion } from 'framer-motion';
import { UFAC_AGENTS } from '@/lib/constants';

// Custom Node Component
function AgentNode({ data }: { data: any }) {
  return (
    <div
      className="px-4 py-3 rounded-lg border-2 shadow-lg"
      style={{
        backgroundColor: data.color,
        borderColor: data.color,
        opacity: data.active ? 1 : 0.6,
      }}
    >
      <Handle type="target" position={Position.Top} />
      <div className="text-white text-center">
        <div className="text-2xl mb-1">{data.icon}</div>
        <div className="font-bold text-sm">{data.label}</div>
        <div className="text-xs opacity-90 mt-1">{data.description}</div>
        {data.consensus && (
          <div className="text-xs mt-2 bg-black/20 rounded px-2 py-1">
            Consensus: {(data.consensus * 100).toFixed(0)}%
          </div>
        )}
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

interface AgentFlowVisualizationProps {
  response?: any;
  isLoading?: boolean;
}

export function AgentFlowVisualization({ response, isLoading }: AgentFlowVisualizationProps) {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedAgent, setSelectedAgent] = useState<string | null>(null);

  // Initialize nodes and edges based on UFAC agents
  useEffect(() => {
    const newNodes: Node[] = [];
    const newEdges: Edge[] = [];

    // Batch 1: Fact, Assumption, Unknown (parallel)
    const batch1Agents = UFAC_AGENTS.filter((a) => a.batch === 1);
    const batch1Y = 50;
    const batch1Spacing = 250;

    batch1Agents.forEach((agent, index) => {
      const xPos = index * batch1Spacing;
      newNodes.push({
        id: agent.id,
        data: {
          label: agent.name,
          description: agent.description,
          color: agent.color,
          icon: agent.icon,
          active: isLoading || !!response,
          consensus: response?.[`${agent.id.split('-')[0]}_consensus`],
        },
        position: { x: xPos, y: batch1Y },
        type: 'default',
      });
    });

    // Batch 2: Confidence, Decision (parallel)
    const batch2Agents = UFAC_AGENTS.filter((a) => a.batch === 2);
    const batch2Y = 250;
    const batch2Spacing = 300;
    const batch2StartX = (batch1Spacing * (batch1Agents.length - 1)) / 2 - batch2Spacing / 2;

    batch2Agents.forEach((agent, index) => {
      const xPos = batch2StartX + index * batch2Spacing;
      newNodes.push({
        id: agent.id,
        data: {
          label: agent.name,
          description: agent.description,
          color: agent.color,
          icon: agent.icon,
          active: isLoading || !!response,
          consensus: response?.[`${agent.id.split('-')[0]}_consensus`],
        },
        position: { x: xPos, y: batch2Y },
        type: 'default',
      });
    });

    // Result node
    newNodes.push({
      id: 'result',
      data: {
        label: 'Eligibility Result',
        description: response?.answer || 'Processing...',
        color: '#06b6d4',
        icon: '🎯',
        active: !!response,
        confidence: response?.confidence,
      },
      position: { x: batch2StartX + batch2Spacing / 2, y: 450 },
      type: 'default',
    });

    // Edges: Batch 1 to Batch 2
    batch1Agents.forEach((agent1) => {
      batch2Agents.forEach((agent2) => {
        newEdges.push({
          id: `${agent1.id}-${agent2.id}`,
          source: agent1.id,
          target: agent2.id,
          animated: isLoading,
          style: { stroke: '#94a3b8', strokeWidth: 2 },
        });
      });
    });

    // Edges: Batch 2 to Result
    batch2Agents.forEach((agent) => {
      newEdges.push({
        id: `${agent.id}-result`,
        source: agent.id,
        target: 'result',
        animated: isLoading,
        style: { stroke: '#06b6d4', strokeWidth: 2 },
      });
    });

    setNodes(newNodes);
    setEdges(newEdges);
  }, [isLoading, response, setNodes, setEdges]);

  const onNodeClick = useCallback((event: React.MouseEvent, node: Node) => {
    setSelectedAgent(node.id);
  }, []);

  return (
    <div className="w-full h-full rounded-lg border border-border bg-card overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick}
        connectionMode={ConnectionMode.Loose}
        nodeTypes={{ default: AgentNode }}
      >
        <Background color="rgba(100, 116, 139, 0.1)" />
        <Controls />
      </ReactFlow>

      {/* Overlay Info */}
      {isLoading && (
        <motion.div
          className="absolute inset-0 flex items-center justify-center bg-black/20 backdrop-blur-sm"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-center text-white">
            <div className="text-4xl mb-4">⚙️</div>
            <p className="text-lg font-semibold">Processing...</p>
            <p className="text-sm opacity-75 mt-2">Running 5 agents in parallel</p>
          </div>
        </motion.div>
      )}
    </div>
  );
}
