"""
Generate Algorithm 1: UFAC Pipeline Pseudocode
Clean algorithm visualization with proper formatting
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Create figure
fig, ax = plt.subplots(figsize=(14, 16))
ax.set_xlim(0, 10)
ax.set_ylim(0, 20)
ax.axis('off')

# Algorithm text with proper indentation
algorithm_lines = [
    ('Algorithm 1: UFAC Eligibility Assessment Pipeline', 'title', 0),
    ('', 'blank', 0),
    ('Input: Farmer query q, Document corpus D, Thresholds θ_high, θ_low', 'io', 0),
    ('Output: Eligibility assessment y', 'io', 0),
    ('', 'blank', 0),
    ('1:  procedure UFAC(q, D, θ_high=75, θ_low=40)', 'proc', 0),
    ('2:      // Retrieval Phase', 'comment', 1),
    ('3:      c ← RETRIEVE(q, D, k=5)              ▷ Get top-k passages', 'code', 1),
    ('4:', 'blank', 0),
    ('5:      // Agent Council Execution (Parallel)', 'comment', 1),
    ('6:      parallel for i ∈ {fact, assm, unk, conf, dec} do', 'loop', 1),
    ('7:          (oᵢ, uᵢ) ← AGENTᵢ(q, c)       ▷ Each agent produces output & uncertainty', 'code', 2),
    ('8:      end parallel', 'loop', 1),
    ('9:', 'blank', 0),
    ('10:     // Uncertainty Aggregation', 'comment', 1),
    ('11:     C ← 100 × (1 - Σᵢ wᵢ · uᵢ)        ▷ Composite confidence score', 'code', 1),
    ('12:', 'blank', 0),
    ('13:     // Routing Decision', 'comment', 1),
    ('14:     R ← 0                                 ▷ Refinement counter', 'code', 1),
    ('15:     while R < R_max and θ_low ≤ C < θ_high do', 'loop', 1),
    ('16:         // Refinement Loop', 'comment', 2),
    ('17:         contradictions ← DETECT_CONFLICTS({o₁, ..., o₅})', 'code', 2),
    ('18:         parallel for i ∈ {fact, assm, unk, conf, dec} do', 'loop', 2),
    ('19:             (oᵢ, uᵢ) ← AGENTᵢ(q, c, oᵢ^prev, contradictions)', 'code', 3),
    ('20:         end parallel', 'loop', 2),
    ('21:         C ← 100 × (1 - Σᵢ wᵢ · uᵢ)    ▷ Recompute confidence', 'code', 2),
    ('22:         R ← R + 1', 'code', 2),
    ('23:     end while', 'loop', 1),
    ('24:', 'blank', 0),
    ('25:     // Final Routing', 'comment', 1),
    ('26:     if C ≥ θ_high then', 'cond', 1),
    ('27:         y ← FINALIZE(o_dec, C)           ▷ Generate final recommendation', 'code', 2),
    ('28:     else if C < θ_low then', 'cond', 1),
    ('29:         y ← ABSTAIN(o_unk, C)            ▷ Return information gap explanation', 'code', 2),
    ('30:     else', 'cond', 1),
    ('31:         y ← PARTIAL_ANSWER(o_dec, C)    ▷ Conditional verdict with hedging', 'code', 2),
    ('32:     end if', 'cond', 1),
    ('33:', 'blank', 0),
    ('34:     return y', 'code', 1),
    ('35: end procedure', 'proc', 0),
]

# Color scheme
colors = {
    'title': '#1976D2',
    'io': '#2E7D32',
    'proc': '#6A1B9A',
    'comment': '#757575',
    'code': '#000000',
    'loop': '#D84315',
    'cond': '#C2185B',
    'blank': '#000000'
}

# Font settings
fonts = {
    'title': {'size': 12, 'weight': 'bold'},
    'io': {'size': 9, 'weight': 'normal', 'style': 'italic'},
    'proc': {'size': 9, 'weight': 'bold'},
    'comment': {'size': 8, 'weight': 'normal', 'style': 'italic'},
    'code': {'size': 8, 'weight': 'normal'},
    'loop': {'size': 9, 'weight': 'bold'},
    'cond': {'size': 9, 'weight': 'bold'},
    'blank': {'size': 8, 'weight': 'normal'}
}

# Background box
box = FancyBboxPatch((0.3, 0.5), 9.4, 18.8, boxstyle="round,pad=0.2",
                      edgecolor='#424242', facecolor='#FAFAFA', linewidth=2)
ax.add_patch(box)

# Render algorithm
y_position = 18.5
line_height = 0.48

for line_text, line_type, indent_level in algorithm_lines:
    if line_type == 'blank':
        y_position -= line_height * 0.5
        continue
    
    # Calculate x position based on indent
    x_position = 0.6 + (indent_level * 0.4)
    
    # Get color and font
    color = colors.get(line_type, '#000000')
    font_props = fonts.get(line_type, {'size': 8, 'weight': 'normal'})
    
    # Render text
    ax.text(x_position, y_position, line_text,
            fontsize=font_props['size'],
            fontweight=font_props.get('weight', 'normal'),
            fontstyle=font_props.get('style', 'normal'),
            color=color,
            family='monospace',
            verticalalignment='top')
    
    y_position -= line_height

plt.tight_layout()
plt.savefig('UFAC_figures/figure_algorithm.pdf', dpi=300, bbox_inches='tight')
plt.savefig('UFAC_figures/figure_algorithm.png', dpi=300, bbox_inches='tight')

print("✓ Algorithm pseudocode generated successfully!")
print("  - figure_algorithm.pdf")
print("  - figure_algorithm.png")
