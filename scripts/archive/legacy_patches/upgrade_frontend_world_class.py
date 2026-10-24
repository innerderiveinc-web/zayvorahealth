import re
import sys

def apply_upgrade():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print(f"Original index.html size: {len(html)} bytes")

    # 1. Add CSS styles for Clinical Thread, Safety Rail, Attention Feed
    css_insert = """
    /* ZAYVORA World-Class Clinical OS Additions */
    .clinical-thread-item {
      transition: all 0.2s ease-in-out;
      cursor: pointer;
    }
    .clinical-thread-item:hover {
      transform: translateY(-1px);
      filter: brightness(1.1);
    }
    .clinical-thread-active {
      border-color: #10B981 !important;
      background: rgba(16, 185, 129, 0.18) !important;
      color: #34D399 !important;
      box-shadow: 0 0 12px rgba(16, 185, 129, 0.25);
    }
    .clinical-thread-completed {
      border-color: rgba(16, 185, 129, 0.4) !important;
      background: rgba(16, 185, 129, 0.08) !important;
      color: #A7F3D0 !important;
    }
    .clinical-thread-pending {
      border-color: rgba(51, 65, 85, 0.6) !important;
      background: rgba(15, 23, 42, 0.6) !important;
      color: #94A3B8 !important;
    }
    .safety-badge-pass {
      background: rgba(16, 185, 129, 0.15);
      color: #34D399;
      border: 1px solid rgba(16, 185, 129, 0.35);
    }
    .safety-badge-caution {
      background: rgba(245, 158, 11, 0.15);
      color: #FBBF24;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }
    .safety-badge-block {
      background: rgba(244, 63, 94, 0.15);
      color: #FB7185;
      border: 1px solid rgba(244, 63, 94, 0.35);
    }
    .safety-badge-unknown {
      background: rgba(148, 163, 184, 0.15);
      color: #CBD5E1;
      border: 1px solid rgba(148, 163, 184, 0.35);
    }
    """

    if '/* ZAYVORA World-Class Clinical OS Additions */' not in html:
        html = html.replace('</style>', css_insert + '\n  </style>', 1)
        print("✓ Injected Clinical Thread & Safety Rail CSS styles")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("✓ Saved updated index.html")

if __name__ == '__main__':
    apply_upgrade()
