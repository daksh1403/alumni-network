from playwright.sync_api import sync_playwright
import argparse

parser = argparse.ArgumentParser(description='Verify every preset button submits its actual SQL without mutating a database.')
parser.add_argument('--url', default='http://localhost:3000/')
args = parser.parse_args()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.route('**/api/**', lambda route: route.fulfill(json={'ok': True, 'kind': 'execute', 'message': 'Regression capture', 'tables': {}, 'stats': {}}))
    page.goto(args.url)
    page.wait_for_load_state('networkidle')
    samples = page.evaluate('SAMPLES')
    for i, sample in enumerate(samples):
        sql = sample[-1]
        with page.expect_response(lambda r: r.url.endswith('/api/query') and r.request.method == 'POST') as response:
            page.locator('.sample').nth(i).click()
        actual = response.value.request.post_data_json['sql']
        assert actual == sql, f'Preset {i+1}: expected SQL {sql!r}, got {actual!r}'
    print(f'PASS: all {len(samples)} preset buttons submit their SQL statements')
    browser.close()
