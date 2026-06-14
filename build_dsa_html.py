import os
import re
import markdown

# Paths
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
MD_PATH = os.path.join(WORKSPACE_DIR, 'DSA', 'dsa.md')
HTML_PATH = os.path.join(WORKSPACE_DIR, 'DSA', 'dsa.html')

def main():
    print(f"Reading markdown from: {MD_PATH}")
    if not os.path.exists(MD_PATH):
        print("Error: dsa.md not found!")
        return

    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert Markdown to HTML
    print("Converting Markdown to HTML...")
    html_body = markdown.markdown(md_content, extensions=['extra', 'toc'])

    # Post-process checklists: replace <li>[ ] and <li>[x] with custom checkboxes
    print("Post-processing checklists...")
    checkpoint_index = 0
    
    def repl_unchecked(match):
        nonlocal checkpoint_index
        content = match.group(1)
        clean_key = re.sub(r'[^a-zA-Z0-9]', '', content).lower()[:30]
        id_str = f"chk-{checkpoint_index}-{clean_key}"
        checkpoint_index += 1
        return f'<li class="task-list-item"><input type="checkbox" id="{id_str}" class="task-checkbox"><span class="task-text">{content}</span></li>'
        
    def repl_checked(match):
        nonlocal checkpoint_index
        content = match.group(1)
        clean_key = re.sub(r'[^a-zA-Z0-9]', '', content).lower()[:30]
        id_str = f"chk-{checkpoint_index}-{clean_key}"
        checkpoint_index += 1
        return f'<li class="task-list-item"><input type="checkbox" id="{id_str}" class="task-checkbox" checked><span class="task-text">{content}</span></li>'

    html_body = re.sub(r'<li>\[\s*\]\s*([\s\S]*?)</li>', repl_unchecked, html_body)
    html_body = re.sub(r'<li>\[[xX]\]\s*([\s\S]*?)</li>', repl_checked, html_body)

    # Wrap the HTML body inside the template
    full_html = get_template(html_body)

    print(f"Writing generated HTML to: {HTML_PATH}")
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Successfully built dsa.html!")

def get_template(html_body):
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSA Revision Handbook — Complete Mastery Guide</title>
    
    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    
    <!-- Prism.js Syntax Highlighting CSS -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">
    
    <style>
        /* CSS variables for consistent premium coloring */
        :root {
            --bg-primary: #07090e;
            --bg-secondary: #0c0f17;
            --bg-sidebar: #090c13;
            --border-color: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --accent-color: #f5a623;
            --accent-hover: #fbbf24;
            --card-bg: #111625;
            --code-bg: #05070a;
            --sidebar-width: 300px;
            --header-height: 60px;
        }

        /* Reset and Base Styles */
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        html {
            scroll-behavior: smooth;
            scroll-padding-top: 80px; /* Offset for scroll targets */
            font-size: 16px;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.625;
            overflow-x: hidden;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #334155;
        }

        /* Layout Structure */
        .app-container {
            display: flex;
            min-height: 100vh;
        }

        /* Mobile Header */
        .mobile-header {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--header-height);
            background-color: var(--bg-sidebar);
            border-bottom: 1px solid var(--border-color);
            align-items: center;
            justify-content: space-between;
            padding: 0 1.5rem;
            z-index: 1000;
        }

        .mobile-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 600;
            color: #fff;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            max-width: 70%;
        }

        .menu-toggle {
            background: none;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 0.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /* Sidebar navigation */
        .sidebar {
            width: var(--sidebar-width);
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            position: fixed;
            top: 0;
            bottom: 0;
            left: 0;
            z-index: 900;
            display: flex;
            flex-direction: column;
            transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .sidebar-header {
            padding: 1.5rem 1.25rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: #fff;
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
        }

        .sidebar-brand svg {
            color: var(--accent-color);
            flex-shrink: 0;
        }

        .sidebar-subtitle {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .search-container {
            padding: 1rem 1.25rem;
            border-bottom: 1px solid var(--border-color);
            position: relative;
        }

        .search-input-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .search-input {
            width: 100%;
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 0.55rem 0.75rem 0.55rem 2.25rem;
            color: #fff;
            font-family: inherit;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 2px rgba(245, 166, 35, 0.15);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            color: var(--text-muted);
            pointer-events: none;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .toc-container {
            flex: 1;
            overflow-y: auto;
            padding: 1rem 0;
        }

        .toc-list {
            list-style: none;
        }

        .toc-item {
            margin: 0.125rem 0;
        }

        .toc-link {
            display: block;
            padding: 0.45rem 1.5rem;
            color: var(--text-secondary);
            font-size: 0.85rem;
            text-decoration: none;
            transition: all 0.15s ease;
            border-left: 2px solid transparent;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .toc-link:hover {
            color: #fff;
            background-color: var(--bg-secondary);
        }

        .toc-link.active {
            color: var(--accent-color);
            font-weight: 600;
            background-color: rgba(245, 166, 35, 0.06);
            border-left-color: var(--accent-color);
        }

        .toc-h1 {
            font-weight: 600;
            color: #cbd5e1;
        }

        .toc-h2 {
            padding-left: 2.25rem;
            font-size: 0.8rem;
        }

        .sidebar-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.55);
            backdrop-filter: blur(2px);
            z-index: 850;
        }

        /* Main Content Panel */
        .main-content {
            margin-left: var(--sidebar-width);
            flex: 1;
            padding: 3rem 4rem 5rem;
            max-width: calc(100% - var(--sidebar-width));
        }

        .content-wrapper {
            max-width: 900px;
            margin: 0 auto;
        }

        /* Markdown Styles & Elements */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            color: #fff;
            font-weight: 600;
            letter-spacing: -0.015em;
            margin-top: 2.75rem;
            margin-bottom: 1rem;
            line-height: 1.25;
        }

        h1 {
            font-size: 2.15rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.6rem;
            margin-top: 3.5rem;
        }

        h2 {
            font-size: 1.55rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-top: 2.5rem;
        }

        h3 {
            font-size: 1.25rem;
            margin-top: 2rem;
        }

        p {
            margin-bottom: 1.25rem;
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.65;
        }

        strong {
            color: #fff;
            font-weight: 600;
        }

        a {
            color: var(--accent-color);
            text-decoration: none;
            border-bottom: 1px dashed transparent;
            transition: all 0.15s ease;
        }

        a:hover {
            color: var(--accent-hover);
            border-bottom-color: var(--accent-hover);
        }

        hr {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, transparent, var(--border-color), transparent);
            margin: 3.5rem 0;
        }

        /* Lists */
        ul, ol {
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        li {
            margin-bottom: 0.5rem;
            line-height: 1.6;
        }

        /* Code Blocks */
        pre {
            margin: 0 !important;
            padding: 1rem !important;
            background-color: var(--code-bg) !important;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            overflow-x: auto;
        }

        code[class*="language-"],
        pre[class*="language-"] {
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 0.85rem !important;
            line-height: 1.6 !important;
            text-shadow: none !important;
            color: #e2e8f0 !important;
        }

        .code-block-wrapper {
            margin: 1.5rem 0;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        }

        .code-block-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 0.45rem 1rem;
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .code-block-wrapper pre {
            border: none;
            border-radius: 0;
        }

        .copy-btn {
            background: none;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            color: var(--text-secondary);
            cursor: pointer;
            font-family: inherit;
            font-size: 0.7rem;
            padding: 0.25rem 0.5rem;
            transition: all 0.15s ease;
            display: flex;
            align-items: center;
            gap: 0.35rem;
        }

        .copy-btn:hover {
            color: #fff;
            background-color: var(--border-color);
            border-color: #475569;
        }

        .icon-svg {
            display: inline-block;
            fill: none;
            stroke: currentColor;
            stroke-width: 2;
            stroke-linecap: round;
            stroke-linejoin: round;
        }

        /* Inline Code */
        p code, li code, blockquote code {
            font-family: 'JetBrains Mono', monospace;
            background-color: rgba(30, 41, 59, 0.4);
            color: var(--accent-hover);
            padding: 0.125rem 0.35rem;
            border-radius: 4px;
            font-size: 0.85rem;
        }

        /* Blockquotes */
        blockquote {
            border-left: 4px solid var(--accent-color);
            background-color: rgba(245, 166, 35, 0.04);
            padding: 1.15rem 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 8px 8px 0;
        }

        blockquote p {
            margin: 0;
            color: #cbd5e1;
            font-style: italic;
        }

        /* Tables styling */
        .table-container {
            width: 100%;
            overflow-x: auto;
            margin: 2rem 0;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            background-color: var(--bg-secondary);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.875rem;
        }

        th {
            background-color: var(--bg-sidebar);
            color: #fff;
            font-weight: 600;
            padding: 0.85rem 1.15rem;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 0.85rem 1.15rem;
            border-bottom: 1px solid var(--border-color);
            color: #cbd5e1;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr:nth-child(even) {
            background-color: rgba(30, 41, 59, 0.2);
        }

        /* Premium Checklist Styling */
        .task-list-item {
            list-style-type: none !important;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.65rem;
            padding: 0.5rem 0.75rem;
            background-color: rgba(30, 41, 59, 0.15);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        .task-list-item:hover {
            border-color: rgba(245, 166, 35, 0.3);
            background-color: rgba(30, 41, 59, 0.25);
        }
        .task-list-item input[type="checkbox"] {
            appearance: none;
            -webkit-appearance: none;
            width: 1.15rem;
            height: 1.15rem;
            border: 2px solid var(--text-muted);
            border-radius: 4px;
            background-color: transparent;
            cursor: pointer;
            display: grid;
            place-content: center;
            transition: all 0.2s ease;
            margin: 0;
            flex-shrink: 0;
        }
        .task-list-item input[type="checkbox"]:checked {
            border-color: var(--accent-color);
            background-color: var(--accent-color);
        }
        .task-list-item input[type="checkbox"]::before {
            content: "";
            width: 0.55rem;
            height: 0.55rem;
            transform: scale(0);
            transition: 120ms transform ease-in-out;
            background-color: var(--bg-primary);
            transform-origin: bottom left;
            clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
        }
        .task-list-item input[type="checkbox"]:checked::before {
            transform: scale(1);
        }
        .task-list-item span {
            font-size: 0.925rem;
            color: var(--text-secondary);
            transition: color 0.2s ease;
        }
        .task-list-item input[type="checkbox"]:checked + span {
            color: var(--text-muted);
            text-decoration: line-through;
        }

        /* Q&A Accordions */
        .qa-accordion {
            margin: 1.5rem 0 2rem 0;
        }

        .qa-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            margin-bottom: 0.75rem;
            overflow: hidden;
            transition: all 0.2s ease;
        }

        .qa-card:hover {
            border-color: var(--accent-color);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }

        .qa-header {
            padding: 1rem 1.25rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            user-select: none;
            font-weight: 600;
            font-size: 0.925rem;
            color: #fff;
            gap: 1.25rem;
        }

        .qa-header-title {
            flex: 1;
            display: flex;
            align-items: flex-start;
            gap: 0.65rem;
        }

        .qa-q-badge {
            background-color: rgba(245, 166, 35, 0.12);
            color: var(--accent-color);
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            font-size: 0.725rem;
            font-weight: 800;
            margin-top: 0.125rem;
            border: 1px solid rgba(245, 166, 35, 0.25);
            display: inline-block;
            line-height: 1;
        }

        .qa-icon {
            font-size: 0.875rem;
            color: var(--text-secondary);
            transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .qa-card.open .qa-icon {
            transform: rotate(180deg);
            color: var(--accent-color);
        }

        .qa-body {
            display: none;
            padding: 1.15rem 1.25rem;
            border-top: 1px solid var(--border-color);
            background-color: var(--bg-primary);
            font-size: 0.9rem;
            color: #cbd5e1;
            line-height: 1.625;
        }

        .qa-body p {
            margin-bottom: 0.75rem;
        }
        .qa-body p:last-child {
            margin-bottom: 0;
        }

        /* Responsive Design Adjustments */
        @media (max-width: 1024px) {
            .sidebar {
                transform: translateX(-100%);
            }
            
            .sidebar.open {
                transform: translateX(0);
            }

            .sidebar-overlay.active {
                display: block;
            }

            .mobile-header {
                display: flex;
            }

            .main-content {
                margin-left: 0;
                max-width: 100%;
                padding: calc(var(--header-height) + 1.5rem) 1.25rem 4rem;
            }
        }

        @media (min-width: 1025px) {
            .sidebar-close-btn {
                display: none;
            }
        }
    </style>
</head>
<body>

    <div class="mobile-header">
        <button class="menu-toggle" id="sidebar-toggle" aria-label="Open navigation menu">
            <svg class="icon-svg" viewBox="0 0 24 24" width="24" height="24">
                <line x1="3" y1="12" x2="21" y2="12"></line>
                <line x1="3" y1="6" x2="21" y2="6"></line>
                <line x1="3" y1="18" x2="21" y2="18"></line>
            </svg>
        </button>
        <span class="mobile-title">DSA Mastery Guide</span>
        <div style="width: 24px;"></div> <!-- Spacer -->
    </div>

    <div class="sidebar-overlay" id="sidebar-overlay"></div>

    <div class="app-container">
        <!-- Sidebar Navigation -->
        <aside class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="sidebar-brand">
                    <svg class="icon-svg" viewBox="0 0 24 24" width="20" height="20" stroke-width="2.5">
                        <path d="M18 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3z"></path>
                        <path d="M6 3a3 3 0 0 0-3 3v12a3 3 0 0 0 3 3 3 3 0 0 0 3-3V6a3 3 0 0 0-3-3z"></path>
                        <path d="M10 6h4"></path>
                        <path d="M10 12h4"></path>
                        <path d="M10 18h4"></path>
                    </svg>
                    <span>DSA Handbook</span>
                </div>
                <div class="sidebar-subtitle">Complete Mastery</div>
            </div>
            
            <div class="search-container">
                <div class="search-input-wrapper">
                    <span class="search-icon">
                        <svg class="icon-svg" viewBox="0 0 24 24" width="16" height="16">
                            <circle cx="11" cy="11" r="8"></circle>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                        </svg>
                    </span>
                    <input type="text" class="search-input" id="search-input" placeholder="Search sections...">
                </div>
            </div>

            <nav class="toc-container">
                <ul class="toc-list" id="toc-list">
                    <!-- TOC elements generated dynamically via JS -->
                </ul>
            </nav>
        </aside>

        <!-- Main Panel Content -->
        <main class="main-content">
            <article class="content-wrapper">
                {html_body}
            </article>
        </main>
    </div>

    <!-- Prism.js Syntax Highlighting Library -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-c.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-cpp.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-java.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>

    <script>
        // DOM Elements
        const sidebar = document.getElementById('sidebar');
        const sidebarToggle = document.getElementById('sidebar-toggle');
        const sidebarOverlay = document.getElementById('sidebar-overlay');
        const searchInput = document.getElementById('search-input');
        const tocList = document.getElementById('toc-list');
        const contentWrapper = document.querySelector('.content-wrapper');

        // 1. Mobile Sidebar Toggle Function
        function toggleSidebar() {
            sidebar.classList.toggle('open');
            sidebarOverlay.classList.toggle('active');
        }

        if (sidebarToggle) sidebarToggle.addEventListener('click', toggleSidebar);
        if (sidebarOverlay) sidebarOverlay.addEventListener('click', toggleSidebar);

        // 2. Code Block Enhancements (Headers, Copy buttons)
        document.querySelectorAll('pre code').forEach((codeEl) => {
            const preEl = codeEl.parentElement;
            
            // Detect language from class e.g., language-cpp
            let lang = 'Plain Text';
            const classes = codeEl.className.split(' ');
            for (const c of classes) {
                if (c.startsWith('language-')) {
                    lang = c.replace('language-', '').toUpperCase();
                    if (lang === 'CPP') lang = 'C++';
                    break;
                }
            }
            
            // Create code block wrapper
            const wrapper = document.createElement('div');
            wrapper.className = 'code-block-wrapper';
            
            // Create header bar
            const header = document.createElement('div');
            header.className = 'code-block-header';
            
            const langSpan = document.createElement('span');
            langSpan.textContent = lang;
            
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = `
                <svg class="icon-svg" viewBox="0 0 24 24" width="12" height="12" stroke-width="2">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                </svg>
                <span>Copy</span>
            `;
            
            copyBtn.addEventListener('click', () => {
                navigator.clipboard.writeText(codeEl.innerText).then(() => {
                    copyBtn.innerHTML = `
                        <svg class="icon-svg" viewBox="0 0 24 24" width="12" height="12" stroke-width="2.5" style="color: #22c55e">
                            <polyline points="20 6 9 17 4 12"></polyline>
                        </svg>
                        <span style="color: #22c55e">Copied!</span>
                    `;
                    setTimeout(() => {
                        copyBtn.innerHTML = `
                            <svg class="icon-svg" viewBox="0 0 24 24" width="12" height="12" stroke-width="2">
                                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                            </svg>
                            <span>Copy</span>
                        `;
                    }, 2000);
                });
            });
            
            header.appendChild(langSpan);
            header.appendChild(copyBtn);
            
            preEl.parentNode.insertBefore(wrapper, preEl);
            wrapper.appendChild(header);
            wrapper.appendChild(preEl);
        });

        // 3. Make all tables responsive
        document.querySelectorAll('table').forEach(table => {
            const container = document.createElement('div');
            container.className = 'table-container';
            table.parentNode.insertBefore(container, table);
            container.appendChild(table);
        });

        // 4. Convert bulleted lists under "Interview Questions" into interactive accordions
        const allHeaders = contentWrapper.querySelectorAll('h1, h2, h3, h4');
        allHeaders.forEach(header => {
            if (header.textContent.toLowerCase().includes('interview questions') || header.textContent.toLowerCase().includes('practice problems')) {
                // Find next sibling list
                let listEl = header.nextElementSibling;
                while (listEl && listEl.tagName !== 'UL' && listEl.tagName !== 'OL' && 
                       listEl.tagName !== 'H1' && listEl.tagName !== 'H2' && listEl.tagName !== 'H3') {
                    listEl = listEl.nextElementSibling;
                }
                
                if (listEl && (listEl.tagName === 'UL' || listEl.tagName === 'OL')) {
                    const items = listEl.querySelectorAll('li');
                    const accordion = document.createElement('div');
                    accordion.className = 'qa-accordion';
                    
                    let hasQAs = false;
                    items.forEach(li => {
                        const text = li.innerText.trim();
                        // Verify this list item represents a Q&A or a question that we can show in accordion
                        // For practice problems, we can also accordion them if they have a description, or keep them
                        if (/^[Q|q]\s*:/i.test(text) && /[A|a]\s*:/i.test(text)) {
                            hasQAs = true;
                            
                            // Extract question text
                            const qMatch = text.match(/^[Q|q]\s*:\s*([\s\S]+?)(?=[A|a]\s*:)/i);
                            const questionText = qMatch ? qMatch[1].trim() : "Interview Question";
                            
                            // DOM-based extraction of answer element (preserves HTML structures)
                            const liClone = li.cloneNode(true);
                            const answerContainer = document.createElement('div');
                            const p = liClone.querySelector('p') || liClone;
                            
                            let foundAnswer = false;
                            const nodes = Array.from(p.childNodes);
                            
                            nodes.forEach(node => {
                                if (foundAnswer) {
                                    answerContainer.appendChild(node);
                                } else if (node.nodeType === Node.TEXT_NODE) {
                                    const aIndex = node.nodeValue.search(/[A|a]\s*:/);
                                    if (aIndex !== -1) {
                                        foundAnswer = true;
                                        node.nodeValue = node.nodeValue.substring(aIndex + 2).trim();
                                        answerContainer.appendChild(node);
                                    }
                                }
                            });
                            
                            // Fallback if DOM extraction fails to find "A:"
                            if (!foundAnswer) {
                                const aMatch = text.match(/[A|a]\s*:\s*([\s\S]+)$/i);
                                answerContainer.textContent = aMatch ? aMatch[1].trim() : text;
                            }
                            
                            // Construct accordion card
                            const card = document.createElement('div');
                            card.className = 'qa-card';
                            
                            const cardHeader = document.createElement('div');
                            cardHeader.className = 'qa-header';
                            
                            const titleSpan = document.createElement('span');
                            titleSpan.className = 'qa-header-title';
                            titleSpan.innerHTML = `<span class="qa-q-badge">Q</span> <span>${questionText}</span>`;
                            
                            const iconSpan = document.createElement('span');
                            iconSpan.className = 'qa-icon';
                            iconSpan.innerHTML = `
                                <svg class="icon-svg" viewBox="0 0 24 24" width="16" height="16">
                                    <polyline points="6 9 12 15 18 9"></polyline>
                                </svg>
                            `;
                            
                            cardHeader.appendChild(titleSpan);
                            cardHeader.appendChild(iconSpan);
                            
                            const cardBody = document.createElement('div');
                            cardBody.className = 'qa-body';
                            cardBody.appendChild(answerContainer);
                            
                            cardHeader.addEventListener('click', () => {
                                const isOpen = card.classList.contains('open');
                                if (isOpen) {
                                    card.classList.remove('open');
                                    cardBody.style.display = 'none';
                                } else {
                                    card.classList.add('open');
                                    cardBody.style.display = 'block';
                                }
                            });
                            
                            card.appendChild(cardHeader);
                            card.appendChild(cardBody);
                            accordion.appendChild(card);
                        }
                    });
                    
                    if (hasQAs) {
                        listEl.parentNode.replaceChild(accordion, listEl);
                    }
                }
            }
        });

        // 5. Generate Table of Contents (TOC) list items
        const headings = contentWrapper.querySelectorAll('h1, h2');
        headings.forEach((heading, idx) => {
            if (!heading.id) {
                heading.id = 'heading-' + idx;
            }
            
            // Skip the TOC heading in the document itself to avoid duplication
            if (heading.id === 'table-of-contents') return;

            const li = document.createElement('li');
            li.className = 'toc-item';
            
            const a = document.createElement('a');
            a.href = '#' + heading.id;
            a.className = 'toc-link ' + (heading.tagName === 'H1' ? 'toc-h1' : 'toc-h2');
            a.textContent = heading.textContent;
            
            // Clean prefix digits if present
            a.textContent = a.textContent.replace(/^\d+\.\s*/, '');
            
            a.addEventListener('click', (e) => {
                if (window.innerWidth <= 1024) {
                    sidebar.classList.remove('open');
                    sidebarOverlay.classList.remove('active');
                }
            });

            li.appendChild(a);
            tocList.appendChild(li);
        });

        // 6. Intersection Observer Scrollspy for Table of Contents
        const tocLinks = document.querySelectorAll('.toc-link');
        const observerOptions = {
            root: null,
            rootMargin: '0px 0px -50% 0px',
            threshold: 0
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.id;
                    tocLinks.forEach(link => {
                        if (link.getAttribute('href') === '#' + id) {
                            link.classList.add('active');
                            link.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
                        } else {
                            link.classList.remove('active');
                        }
                    });
                }
            });
        }, observerOptions);

        headings.forEach(h => {
            if (h.id !== 'table-of-contents') {
                observer.observe(h);
            }
        });

        // 7. Sidebar Filter / Search functionality
        searchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            tocLinks.forEach(link => {
                const text = link.textContent.toLowerCase();
                const parent = link.parentElement;
                if (text.includes(query)) {
                    parent.style.display = 'block';
                } else {
                    parent.style.display = 'none';
                }
            });
        });

        // 8. Fuzzy scroll target matching for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(link => {
            link.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href').substring(1);
                if (!targetId) return;
                
                let target = document.getElementById(targetId);
                
                // Fuzzy matching search for IDs
                if (!target) {
                    const normalize = str => str.toLowerCase().replace(/[^a-z0-9]/g, '');
                    const normalizedTarget = normalize(targetId);
                    
                    const allPageElements = contentWrapper.querySelectorAll('h1, h2, h3, h4, h5, h6');
                    for (const el of allPageElements) {
                        if (normalize(el.id) === normalizedTarget || normalize(el.textContent).includes(normalizedTarget)) {
                            target = el;
                            break;
                        }
                    }
                }
                
                if (target) {
                    e.preventDefault();
                    target.scrollIntoView({ behavior: 'smooth' });
                    history.pushState(null, null, '#' + target.id);
                }
            });
        });

        // 9. Checkbox state persistence in localStorage
        const checkboxes = document.querySelectorAll('.task-checkbox');
        checkboxes.forEach(cb => {
            // Restore state
            const saved = localStorage.getItem(cb.id);
            if (saved === 'true') {
                cb.checked = true;
                const span = cb.nextElementSibling;
                if (span) span.style.textDecoration = 'line-through';
            } else if (saved === 'false') {
                cb.checked = false;
                const span = cb.nextElementSibling;
                if (span) span.style.textDecoration = 'none';
            }

            // Save state on change
            cb.addEventListener('change', (e) => {
                localStorage.setItem(cb.id, cb.checked);
                const span = cb.nextElementSibling;
                if (span) {
                    if (cb.checked) {
                        span.style.textDecoration = 'line-through';
                    } else {
                        span.style.textDecoration = 'none';
                    }
                }
            });
        });
    </script>
</body>
</html>"""
    return template.replace("{html_body}", html_body)

if __name__ == '__main__':
    main()
