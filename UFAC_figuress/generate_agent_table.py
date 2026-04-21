"""
Generate Agent Specification Table
Clean table showing all 5 agents with their roles, inputs, outputs, uncertainty signals, and weights
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Create figure
fig, ax = plt.subplots(figsize=(16, 10))
ax.axis('tight')
ax.axis('off')

# Table data
headers = ['Agent', 'Role', 'Primary Input', 'Output Format', 'Uncertainty Signal', 'Weight\n(wᵢ)']

data = [
    ['Fact Agent\n(A_fact)',
     'Strictly extractive reasoning.\nExtract only claims directly\nattested in retrieved passages\nwith explicit clause attribution.',
     'Query q,\nContext c',
     '{facts: [...],\nattributions: [...]}',
     'u₁ = (# unattributable claims) /\n(total claims + ε) +\nδ_miss × (# withheld claims)',
     '0.35'],
    
    ['Assumption\nAgent\n(A_assm)',
     'Identify implicit premises in\nquery or Fact output not\nconfirmed by context.\nAssign support scores.',
     'Query q,\nContext c,\nFact output',
     '{assumptions: [...],\nsupport_scores: [...]}',
     'u₂ = (# unverifiable assumptions) /\n(total assumptions + ε)',
     '0.20'],
    
    ['Unknown\nAgent\n(A_unk)',
     'Detect critical information\nabsent from context.\nDistinguish Type I vs Type II\ngaps.',
     'Query q,\nContext c,\nPolicy schema',
     '{unknowns: [...],\ntypes: [...],\nseverity: [...]}',
     'u₃ = severity_weight ×\n(# high-severity gaps) /\n(total gaps + ε)',
     '0.20'],
    
    ['Confidence\nAgent\n(A_conf)',
     'Aggregate u₁, u₂, u₃ into\ncomposite confidence C.\nCompute internal consistency.',
     'Outputs\n{o₁, o₂, o₃},\nUncertainties\n{u₁, u₂, u₃}',
     '{confidence_score: C,\ninternal_consistency: IC,\nECE: float}',
     'u₄ = 1 - IC\n(internal consistency measure)',
     '0.25'],
    
    ['Decision\nAgent\n(A_dec)',
     'Synthesize final farmer-facing\nrecommendation with verdict,\nevidence, documents, deadlines,\nand hedging.',
     'All outputs\n{o₁,...,o₄},\nConfidence C,\nRouting decision',
     '{verdict: {...},\nevidence: [...],\ndocuments: [...],\ndeadline: str,\nhedging: [...]}',
     'u₅ = (# hedging statements) /\n(total statements + ε)',
     '—']
]

# Create table
table = ax.table(cellText=data, colLabels=headers,
                cellLoc='left', loc='center',
                colWidths=[0.12, 0.22, 0.14, 0.16, 0.26, 0.08])

# Style the table
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 3)

# Header styling
for i in range(len(headers)):
    cell = table[(0, i)]
    cell.set_facecolor('#2196F3')
    cell.set_text_props(weight='bold', color='white', fontsize=9)
    cell.set_height(0.08)

# Row colors (alternating)
colors = ['#E3F2FD', '#FFFFFF']
for i in range(1, len(data) + 1):
    for j in range(len(headers)):
        cell = table[(i, j)]
        cell.set_facecolor(colors[(i-1) % 2])
        cell.set_edgecolor('#BDBDBD')
        cell.set_linewidth(1.5)
        
        # Bold agent names
        if j == 0:
            cell.set_text_props(weight='bold', fontsize=8)
        
        # Bold weights
        if j == 5:
            cell.set_text_props(weight='bold', fontsize=9, ha='center')

# Title
fig.suptitle('UFAC Agent Specifications', fontsize=14, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig('UFAC_figures/figure_agent_table.pdf', dpi=300, bbox_inches='tight')
plt.savefig('UFAC_figures/figure_agent_table.png', dpi=300, bbox_inches='tight')

print("✓ Agent specification table generated successfully!")
print("  - figure_agent_table.pdf")
print("  - figure_agent_table.png")
