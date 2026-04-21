"""
Generate UFAC System Architecture Diagram
Clean block diagram showing the 4-stage pipeline with proper flow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Wedge
import matplotlib.lines as mlines

# Create figure
fig, ax = plt.subplots(figsize=(14, 18))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# Color palette
color_doc = '#E3F2FD'  # Light blue - document processing
color_retrieval = '#2196F3'  # Blue - retrieval
color_agent = '#4CAF50'  # Green - agents
color_uncertainty = '#FF9800'  # Orange - uncertainty
color_routing = '#9C27B0'  # Purple - routing
color_output = '#009688'  # Teal - output

# Helper function to create rounded boxes
def create_box(ax, x, y, width, height, text, color, fontsize=10, fontweight='normal'):
    box = FancyBboxPatch((x, y), width, height, boxstyle="round,pad=0.1",
                          edgecolor='black', facecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(x + width/2, y + height/2, text, ha='center', va='center',
            fontsize=fontsize, fontweight=fontweight, wrap=True)

# Helper function for arrows
def create_arrow(ax, x1, y1, x2, y2, label='', color='black', width=2):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                           arrowstyle='->', mutation_scale=20,
                           color=color, linewidth=width)
    ax.add_patch(arrow)
    if label:
        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
        ax.text(mid_x + 0.3, mid_y, label, fontsize=8, style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

# ===== STAGE 1: Document Ingestion =====
y_pos = 18.5
ax.text(0.2, y_pos, 'STAGE 1', fontsize=11, fontweight='bold', color='#1976D2')
ax.text(1.5, y_pos, 'Document Ingestion', fontsize=10, style='italic', color='#666')

create_box(ax, 1, 17.2, 8, 0.8, 
           'Document Corpus\n68 official GoI policy documents (PM-KISAN, PMFBY, PM-KUSUM, SHC, KCC, PM-DDKY)',
           color_doc, fontsize=9, fontweight='bold')

create_box(ax, 1.5, 15.5, 7, 1.3,
           'Preprocessing Pipeline\n• Structural cleaning  • Text normalization\n• Lemmatization  • Segmentation (512-token passages, 64-token overlap)',
           color_doc, fontsize=8)

create_arrow(ax, 5, 17.2, 5, 16.8)

# ===== STAGE 2: Retrieval =====
y_pos = 14.5
ax.text(0.2, y_pos, 'STAGE 2', fontsize=11, fontweight='bold', color='#1976D2')
ax.text(1.5, y_pos, 'Retrieval', fontsize=10, style='italic', color='#666')

create_box(ax, 1.5, 13, 7, 0.9,
           'ChromaDB Vector Store\nSentenceTransformer (all-MiniLM-L6-v2) • 384-dim embeddings',
           color_retrieval, fontsize=8, fontweight='bold')

# Farmer query input
create_box(ax, 0.3, 12.2, 1.8, 0.6,
           'Farmer\nQuery q',
           '#FFE082', fontsize=8, fontweight='bold')
create_arrow(ax, 2.1, 12.5, 2.8, 13.2, '', '#FF6F00', 2)

create_box(ax, 2, 11.5, 6, 0.8,
           'Retrieval Module: embed query, retrieve top-k=5, cosine threshold 0.45',
           color_retrieval, fontsize=8)

create_arrow(ax, 5, 13, 5, 12.3, 'Context c\n(k passages)', '#1976D2', 3)

# ===== STAGE 3: Five-Agent Council =====
y_pos = 10.5
ax.text(0.2, y_pos, 'STAGE 3', fontsize=11, fontweight='bold', color='#1976D2')
ax.text(1.5, y_pos, 'Five-Agent Council (Parallel Execution)', fontsize=10, style='italic', color='#666')

# Five agents in a row
agent_y = 8.5
agent_width = 1.6
agent_height = 1.3
agent_spacing = 0.2

agents = [
    ('Fact Agent\nA_fact\n\nw=0.35', 1),
    ('Assumption\nAgent\nA_assm\nw=0.20', 1 + agent_width + agent_spacing),
    ('Unknown\nAgent\nA_unk\nw=0.20', 1 + 2*(agent_width + agent_spacing)),
    ('Confidence\nAgent\nA_conf\nw=0.25', 1 + 3*(agent_width + agent_spacing)),
    ('Decision\nAgent\nA_dec', 1 + 4*(agent_width + agent_spacing))
]

# Draw arrows from retrieval to first 3 agents
for i in range(3):
    x_pos = agents[i][1] + agent_width/2
    create_arrow(ax, 5, 11.5, x_pos, agent_y + agent_height, '', '#666', 1.5)

# Draw agents
for agent_text, x_pos in agents:
    create_box(ax, x_pos, agent_y, agent_width, agent_height,
               agent_text, color_agent, fontsize=7, fontweight='bold')

# Arrows between agents (Fact, Assm, Unk → Conf → Dec)
for i in range(3):
    x_from = agents[i][1] + agent_width/2
    x_to = agents[3][1] + agent_width/2
    create_arrow(ax, x_from, agent_y, x_to, agent_y + agent_height/2, '', '#2E7D32', 1)

create_arrow(ax, agents[3][1] + agent_width/2, agent_y,
             agents[4][1] + agent_width/2, agent_y + agent_height/2, '', '#2E7D32', 1)

# Uncertainty aggregator
create_box(ax, 2, 7, 6, 0.7,
           'Uncertainty Aggregator: C = 100·(1 − Σᵢ wᵢ uᵢ)',
           color_uncertainty, fontsize=9, fontweight='bold')

create_arrow(ax, agents[3][1] + agent_width/2, agent_y, 5, 7.7, '', '#E65100', 2)

# ===== STAGE 4: Routing and Outputs =====
y_pos = 6
ax.text(0.2, y_pos, 'STAGE 4', fontsize=11, fontweight='bold', color='#1976D2')
ax.text(1.5, y_pos, 'Routing and Outputs', fontsize=10, style='italic', color='#666')

# Diamond routing decision
diamond_x, diamond_y = 5, 4.5
diamond_size = 0.8
diamond = mpatches.FancyBboxPatch((diamond_x - diamond_size/2, diamond_y - diamond_size/2),
                                   diamond_size, diamond_size,
                                   boxstyle="round,pad=0.05", transform=ax.transData,
                                   edgecolor='black', facecolor=color_routing, linewidth=2)
ax.add_patch(diamond)
ax.text(diamond_x, diamond_y, 'Routing\nC-based', ha='center', va='center',
        fontsize=8, fontweight='bold')

create_arrow(ax, 5, 7, 5, 5.3, '', '#6A1B9A', 2)

# Three output boxes
output_y = 2.5
output_width = 2.2
output_height = 1

outputs = [
    ('FINALIZE\nC ≥ 75\n\nStructured\nrecommendation', 1.2),
    ('REFINE\n40 ≤ C < 75\n\nRe-run agents\n(R≤2)', 4.4),
    ('ABSTAIN\nC < 40\n\nInformation\ngaps', 7.6)
]

for text, x_pos in outputs:
    create_box(ax, x_pos, output_y, output_width, output_height,
               text, color_output, fontsize=7, fontweight='bold')

# Arrows from routing to outputs
create_arrow(ax, diamond_x - 0.5, diamond_y, outputs[0][1] + output_width/2, output_y + output_height,
             '', '#00695C', 1.5)
create_arrow(ax, diamond_x, diamond_y - 0.5, outputs[1][1] + output_width/2, output_y + output_height,
             '', '#00695C', 1.5)
create_arrow(ax, diamond_x + 0.5, diamond_y, outputs[2][1] + output_width/2, output_y + output_height,
             '', '#00695C', 1.5)

# Feedback loop from REFINE back to agents (dashed)
ax.annotate('', xy=(agents[0][1], agent_y + agent_height/2), xytext=(outputs[1][1] + output_width, output_y + output_height/2),
            arrowprops=dict(arrowstyle='->', lw=1.5, linestyle='--', color='#D32F2F'))
ax.text(0.5, 5.5, 'Feedback\nLoop', fontsize=7, style='italic', color='#D32F2F',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))

# Final output box
create_box(ax, 2.5, 0.5, 5, 0.8,
           'Final Output: verdict + evidence + checklist + deadlines + hedging',
           '#B2DFDB', fontsize=8, fontweight='bold')

for x_pos in [outputs[0][1] + output_width/2, outputs[1][1] + output_width/2, outputs[2][1] + output_width/2]:
    create_arrow(ax, x_pos, output_y, 5, 1.3, '', '#004D40', 1.5)

plt.tight_layout()
plt.savefig('UFAC_figures/figure_architecture.pdf', dpi=300, bbox_inches='tight')
plt.savefig('UFAC_figures/figure_architecture.png', dpi=300, bbox_inches='tight')

print("✓ Architecture diagram generated successfully!")
print("  - figure_architecture.pdf")
print("  - figure_architecture.png")
