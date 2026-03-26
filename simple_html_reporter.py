"""
简单可靠的静态HTML报告生成器
完全不依赖JavaScript，任何浏览器都能正常显示
支持显示中文标题和请求响应日志
"""
import os
import json
from datetime import datetime


def generate_html_report(json_results_path, html_output_path):
    """
    从pytest的JSON结果生成静态HTML报告
    
    Args:
        json_results_path: pytest JSON结果文件路径
        html_output_path: 输出的HTML文件路径
    """
    with open(json_results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 加载测试用例额外信息（中文标题、请求响应等）
    test_case_info = {}
    test_case_info_path = os.path.join(os.path.dirname(json_results_path), 'test_case_info.json')
    if os.path.exists(test_case_info_path):
        with open(test_case_info_path, 'r', encoding='utf-8') as f:
            test_case_info = json.load(f)
    
    # 统计数据
    total = 0
    passed = 0
    failed = 0
    skipped = 0
    error = 0
    xfailed = 0
    xpassed = 0
    
    test_cases = []
    
    for test in data.get('tests', []):
        total += 1
        outcome = test.get('outcome', 'unknown')
        nodeid = test.get('nodeid', '')
        duration = test.get('setup', {}).get('duration', 0) + \
                   test.get('call', {}).get('duration', 0) + \
                   test.get('teardown', {}).get('duration', 0)
        
        # 获取中文标题
        case_info = test_case_info.get(nodeid, {})
        chinese_title = case_info.get('chinese_title', nodeid.split('::')[-1])
        requests = case_info.get('requests', [])
        
        # 获取错误信息
        error_msg = ''
        if outcome == 'failed':
            call = test.get('call', {})
            if call.get('crash'):
                error_msg = call['crash'].get('message', '')
                error_msg += '\n' + call['crash'].get('traceback', '')
        
        test_cases.append({
            'name': nodeid,
            'chinese_title': chinese_title,
            'outcome': outcome,
            'duration': duration,
            'error': error_msg,
            'requests': requests
        })
        
        if outcome == 'passed':
            passed += 1
        elif outcome == 'failed':
            failed += 1
        elif outcome == 'skipped':
            skipped += 1
        elif outcome == 'error':
            error += 1
        elif outcome == 'xfailed':
            xfailed += 1
        elif outcome == 'xpassed':
            xpassed += 1
    
    # 生成HTML
    html_content = _build_html(total, passed, failed, skipped, error, xfailed, xpassed, test_cases)
    
    with open(html_output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def _build_html(total, passed, failed, skipped, error, xfailed, xpassed, test_cases):
    """构建HTML内容"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试报告 - {now}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{ max-width: 1400px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; border-radius: 8px 8px 0 0;
        }}
        .header h1 {{ font-size: 28px; margin-bottom: 10px; }}
        .header p {{ font-size: 14px; opacity: 0.9; }}
        .summary {{ display: flex; flex-wrap: wrap; padding: 20px; gap: 15px; border-bottom: 1px solid #eee; }}
        .stat-card {{ 
            flex: 1; min-width: 120px; padding: 20px; border-radius: 8px; 
            text-align: center; color: white;
        }}
        .stat-card .num {{ font-size: 32px; font-weight: bold; }}
        .stat-card .label {{ font-size: 14px; margin-top: 5px; }}
        .total {{ background: #6c757d; }}
        .passed {{ background: #28a745; }}
        .failed {{ background: #dc3545; }}
        .skipped {{ background: #ffc107; color: #333; }}
        .error {{ background: #fd7e14; }}
        .xfailed {{ background: #17a2b8; }}
        .xpassed {{ background: #6f42c1; }}
        .content {{ padding: 20px; }}
        .test-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .test-table th, .test-table td {{ 
            padding: 12px 15px; text-align: left; border-bottom: 1px solid #eee;
        }}
        .test-table th {{ 
            background: #f8f9fa; font-weight: 600; color: #495057;
        }}
        .test-table tr:hover {{ background: #f8f9fa; }}
        .badge {{ 
            display: inline-block; padding: 4px 12px; border-radius: 12px; 
            font-size: 12px; font-weight: 600;
        }}
        .badge-passed {{ background: #d4edda; color: #155724; }}
        .badge-failed {{ background: #f8d7da; color: #721c24; }}
        .badge-skipped {{ background: #fff3cd; color: #856404; }}
        .badge-error {{ background: #ffe5d0; color: #9f4c00; }}
        .badge-xfailed {{ background: #d1ecf1; color: #0c5460; }}
        .badge-xpassed {{ background: #e2d5f1; color: #48257a; }}
        .test-name {{ 
            font-family: 'Courier New', monospace; font-size: 12px; color: #666;
            word-break: break-all; margin-top: 4px;
        }}
        .test-title {{
            font-size: 15px; font-weight: 600; color: #333;
        }}
        .error-details {{ 
            margin-top: 8px; padding: 10px; background: #fff5f5; 
            border-left: 3px solid #dc3545; border-radius: 4px;
            font-family: 'Courier New', monospace; font-size: 12px;
            white-space: pre-wrap; max-height: 200px; overflow-y: auto;
        }}
        .duration {{ color: #6c757d; font-size: 13px; }}
        .requests-section {{
            margin-top: 10px;
        }}
        .request-item {{
            background: #f8f9fa;
            border-radius: 6px;
            padding: 12px;
            margin-top: 8px;
            border: 1px solid #e9ecef;
        }}
        .request-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }}
        .request-method {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            color: white;
        }}
        .method-GET {{ background: #61affe; }}
        .method-POST {{ background: #49cc90; }}
        .method-PUT {{ background: #fca130; }}
        .method-DELETE {{ background: #f93e3e; }}
        .request-url {{
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #333;
            flex: 1;
            margin-left: 10px;
            word-break: break-all;
        }}
        .request-body, .response-body {{
            margin-top: 8px;
            padding: 8px;
            background: white;
            border-radius: 4px;
            border: 1px solid #dee2e6;
            font-family: 'Courier New', monospace;
            font-size: 11px;
            white-space: pre-wrap;
            max-height: 300px;
            overflow-y: auto;
        }}
        .section-title {{
            font-size: 12px;
            font-weight: 600;
            color: #495057;
            margin-top: 8px;
            margin-bottom: 4px;
        }}
        .toggle-btn {{
            background: #e9ecef;
            border: none;
            padding: 4px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            color: #495057;
        }}
        .toggle-btn:hover {{
            background: #dee2e6;
        }}
        .collapsible {{
            display: none;
        }}
        .collapsible.show {{
            display: block;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧪 若依后台管理系统 - API测试报告</h1>
            <p>生成时间: {now}</p>
        </div>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="num">{total}</div>
                <div class="label">总用例数</div>
            </div>
            <div class="stat-card passed">
                <div class="num">{passed}</div>
                <div class="label">通过</div>
            </div>
            <div class="stat-card failed">
                <div class="num">{failed}</div>
                <div class="label">失败</div>
            </div>
            <div class="stat-card skipped">
                <div class="num">{skipped}</div>
                <div class="label">跳过</div>
            </div>
            {f'''<div class="stat-card error">
                <div class="num">{error}</div>
                <div class="label">错误</div>
            </div>''' if error > 0 else ''}
            {f'''<div class="stat-card xfailed">
                <div class="num">{xfailed}</div>
                <div class="label">预期失败</div>
            </div>''' if xfailed > 0 else ''}
            {f'''<div class="stat-card xpassed">
                <div class="num">{xpassed}</div>
                <div class="label">意外通过</div>
            </div>''' if xpassed > 0 else ''}
        </div>
        
        <div class="content">
            <h2 style="margin-bottom: 10px; color: #333;">📋 测试用例详情</h2>
            <table class="test-table">
                <thead>
                    <tr>
                        <th style="width: 80px;">状态</th>
                        <th>测试用例</th>
                        <th style="width: 100px;">耗时</th>
                    </tr>
                </thead>
                <tbody>
                    {_build_test_rows(test_cases)}
                </tbody>
            </table>
        </div>
    </div>
    <script>
        function toggleRequests(id) {{
            var element = document.getElementById('requests-' + id);
            var btn = document.getElementById('btn-' + id);
            if (element.classList.contains('show')) {{
                element.classList.remove('show');
                btn.textContent = '显示请求/响应';
            }} else {{
                element.classList.add('show');
                btn.textContent = '隐藏请求/响应';
            }}
        }}
    </script>
</body>
</html>"""


def _build_test_rows(test_cases):
    """构建测试用例行"""
    rows = []
    for idx, tc in enumerate(test_cases):
        outcome = tc['outcome']
        badge_class = f'badge-{outcome}'
        duration = f"{tc['duration']:.3f}s"
        
        error_html = ''
        if tc.get('error'):
            error_html = f'<div class="error-details">{_escape_html(tc["error"])}</div>'
        
        requests_html = _build_requests_html(tc.get('requests', []), idx)
        
        rows.append(f"""<tr>
            <td><span class="badge {badge_class}">{outcome.upper()}</span></td>
            <td>
                <div class="test-title">{_escape_html(tc['chinese_title'])}</div>
                <div class="test-name">{_escape_html(tc['name'])}</div>
                {error_html}
                {requests_html}
            </td>
            <td class="duration">{duration}</td>
        </tr>""")
    return '\n'.join(rows)


def _build_requests_html(requests, idx):
    """构建请求响应HTML"""
    if not requests:
        return ''
    
    html_parts = []
    for req_idx, req_data in enumerate(requests):
        req = req_data.get('request', {})
        resp = req_data.get('response', {})
        
        method = req.get('method', 'GET')
        url = req.get('url', '')
        
        request_body = ''
        if req.get('json'):
            request_body = json.dumps(req['json'], ensure_ascii=False, indent=2)
        elif req.get('params'):
            request_body = json.dumps(req['params'], ensure_ascii=False, indent=2)
        
        response_body = ''
        if resp.get('json'):
            response_body = json.dumps(resp['json'], ensure_ascii=False, indent=2)
        elif resp.get('text'):
            response_body = resp['text']
        
        status_code = resp.get('status_code', '')
        
        html_parts.append(f"""
        <div class="request-item">
            <div class="request-header">
                <span class="request-method method-{method}">{method}</span>
                <span class="request-url">{_escape_html(url)}</span>
                <span style="margin-left: 10px; font-size: 12px; color: #666;">
                    Status: <strong>{status_code}</strong>
                </span>
            </div>
            {f'''
            <div class="section-title">📤 请求体:</div>
            <div class="request-body">{_escape_html(request_body)}</div>
            ''' if request_body else ''}
            {f'''
            <div class="section-title">📥 响应体:</div>
            <div class="response-body">{_escape_html(response_body)}</div>
            ''' if response_body else ''}
        </div>
        """)
    
    return f"""
    <div class="requests-section">
        <button class="toggle-btn" id="btn-{idx}" onclick="toggleRequests({idx})">显示请求/响应</button>
        <div class="collapsible" id="requests-{idx}">
            {"".join(html_parts)}
        </div>
    </div>
    """


def _escape_html(text):
    """转义HTML特殊字符"""
    if not isinstance(text, str):
        text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    return text
