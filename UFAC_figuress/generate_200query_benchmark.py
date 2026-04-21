"""
Generate 200-Query Benchmark Distribution Figure
Three-panel visualization showing query categories, verdict distribution, and queries per scheme
"""

import matplotlib.pyplot as plt
import numpy as np

# Data for 200-query benchmark
# Category distribution
categories = ['Direct\nEligibility', 'Document\nChecklist', 'Benefit &\nDeadline', 'Cross-Scheme\nInteraction']
category_counts = [80, 50, 40, 30]

# Verdict distribution
verdicts = ['ELIGIBLE', 'INELIGIBLE', 'ABSTAIN']
verdict_counts = [110, 52, 38]  # 55%, 26%, 19%
verdict_colors = ['#2ecc71', '#e74c3c', '#f39c12']

# Queries per scheme
schemes = ['PM-KISAN', 'PMFBY', 'PM-KUSUM', 'KCC', 'SHC', 'PM-DDKY']
scheme_counts = [55, 42, 30, 30, 25, 18]

# Create figure with 3 subplots
fig = plt.figure(figsize=(16, 5))

# Subplot 1: Query Categories (Bar Chart)
ax1 = fig.add_subplot(131)
bars1 = ax1.bar(categories, category_counts, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Number of Queries', fontsize=11, fontweight='bold')
ax1.set_title('Query Category Distribution', fontsize=12, fontweight='bold')
ax1.set_ylim([0, 90])
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# Add value labels on bars
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'n={int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Subplot 2: Verdict Distribution (Pie Chart)
ax2 = fig.add_subplot(132)
wedges, texts, autotexts = ax2.pie(verdict_counts, labels=verdicts, colors=verdict_colors,
                                     autopct='%1.0f%%', startangle=90,
                                     textprops={'fontsize': 11, 'fontweight': 'bold'},
                                     wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})

# Add counts to labels
for i, (text, count) in enumerate(zip(texts, verdict_counts)):
    text.set_text(f'{verdicts[i]}\n(n={count})')
    text.set_fontsize(10)
    text.set_fontweight('bold')

ax2.set_title('Gold-Label Verdict Distribution', fontsize=12, fontweight='bold')

# Subplot 3: Queries per Scheme (Horizontal Bar Chart)
ax3 = fig.add_subplot(133)
y_pos = np.arange(len(schemes))
bars3 = ax3.barh(y_pos, scheme_counts, color='#9b59b6', alpha=0.8, edgecolor='black', linewidth=1.5)
ax3.set_yticks(y_pos)
ax3.set_yticklabels(schemes, fontsize=10)
ax3.set_xlabel('Number of Queries', fontsize=11, fontweight='bold')
ax3.set_title('Queries per Scheme', fontsize=12, fontweight='bold')
ax3.set_xlim([0, 60])
ax3.grid(axis='x', alpha=0.3, linestyle='--')
ax3.invert_yaxis()  # Highest count at top

# Add value labels on bars
for i, (bar, count) in enumerate(zip(bars3, scheme_counts)):
    width = bar.get_width()
    ax3.text(width, bar.get_y() + bar.get_height()/2.,
            f' n={int(count)}', ha='left', va='center', fontsize=10, fontweight='bold')

# Overall title
fig.suptitle('UFAC 200-Query Benchmark: Distribution Analysis', 
             fontsize=14, fontweight='bold', y=1.02)

plt.tight_layout()

# Save figure
plt.savefig('UFAC_figures/figure_benchmark_200query.pdf', dpi=300, bbox_inches='tight')
plt.savefig('UFAC_figures/figure_benchmark_200query.png', dpi=300, bbox_inches='tight')

print("✓ 200-query benchmark figure generated successfully!")
print("  - figure_benchmark_200query.pdf")
print("  - figure_benchmark_200query.png")
