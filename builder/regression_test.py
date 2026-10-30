from playwright.sync_api import sync_playwright
from pathlib import Path
import re,json,os
_src=Path(__file__).resolve().parent.parent/'index.html'
html=re.sub(r'<script[^>]+src="https://[^"]+"[^>]*></script>','',_src.read_text())
_chrome='/usr/bin/chromium' if os.path.exists('/usr/bin/chromium') else '/usr/bin/google-chrome'
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=_chrome,args=['--no-sandbox','--disable-dev-shm-usage'])
 ctx=browser.new_context(viewport={'width':1200,'height':850})
 page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 page.set_content(html,wait_until='domcontentloaded');page.wait_for_selector('.hero')
 # Check core curriculum data and all labs
 assert page.evaluate('WEEKS.length')==9
 assert page.evaluate('ALL_DAYS.length')==63
 assert page.evaluate('LABS.length')==32
 assert page.evaluate('Object.keys(CHALLENGES).length')==63
 assert page.evaluate('WEEKS.every(w=>w.days.every(d=>d.questions.length===4 && d.objectives.length>=6 && d.readings.length>=5))')
 assert page.evaluate('WEEKS.reduce((s,w)=>s+w.resources.length,0)')>=90
 page.locator('[data-action="nav"][data-route="labs"]').click()
 for lab_id in page.evaluate('LABS.map(l=>l.id)'):
   page.locator(f'[data-action="lab-select"][data-lab="{lab_id}"]').click()
   s=page.locator('#labOutput').inner_text()
   assert s and len(s)>30,(lab_id,s)
   json_out=page.evaluate('window.currentLabResult')
   assert json_out['lab']==lab_id,lab_id
 print('PASS: all 32 labs compute results, output snapshots, and render')
 # Dynamic custom lab and its editable formula
 page.locator('[data-action="lab-create"]').click()
 page.locator('input[name="title"]').fill('Tiny custom sigmoid')
 page.locator('[data-smart="custom-formula"] .smart-trigger').click()
 page.locator('[data-key="custom-formula"][data-value="sigmoid"]').click()
 page.locator('#customLabForm button[type="submit"]').click()
 assert page.evaluate('state.customLabs.length')==1
 assert page.evaluate('state.customLabs[0].formula')=='sigmoid'
 assert len(page.locator('#labOutput').inner_text())>20
 print('PASS: create and calculate custom lab')
 # Quiz full pass and separate direct mark
 page.locator('[data-action="nav"][data-route="learn"]').click()
 assert not page.evaluate('done("d1")')
 page.locator('[data-action="lesson-tab"][data-tab="quiz"]').click()
 correct=page.evaluate('ALL_DAYS[0].questions.map(q=>q.correct)')
 for i,choice in enumerate(correct):
   page.locator(f'[data-action="quiz-choice"][data-question="{i}"][data-choice="{choice}"]').click()
 page.locator('[data-action="quiz-submit"]').click()
 assert page.evaluate('dayState("d1").quizPassed')
 assert page.evaluate('dayState("d1").quizHistory[0].score')==4
 assert not page.evaluate('done("d1")'), 'quiz pass must not falsely mark unpracticed day done'
 page.locator('[data-action="mark-day"]').click()
 assert page.evaluate('done("d1")')
 assert page.evaluate('dayState("d1").manualComplete')
 page.locator('[data-action="mark-day"]').click()
 assert not page.evaluate('done("d1")')
 assert page.evaluate('dayState("d1").quizPassed'),'reopening must retain prior quiz mastery'
 print('PASS: quiz scoring, mastery separation, direct mark / reopen')
 # Week switching custom dropdown
 page.locator('[data-smart="week"] .smart-trigger').click()
 page.locator('[data-key="week"][data-value="2"]').click()
 assert page.evaluate('ui.week')==2
 assert page.locator('h2.lesson-title').inner_text().startswith('PyTorch')
 print('PASS: custom dropdown changes week and lesson')
 # Focus preferences, complete session via mock time advance
 page.locator('[data-action="nav"][data-route="settings"]').click()
 page.locator('[data-change="focus-minutes"]').fill('1')
 page.locator('[data-change="focus-minutes"]').dispatch_event('change')
 assert page.evaluate('state.settings.focusMinutes')==1
 page.locator('[data-action="timer-toggle"]').click()
 assert page.evaluate('timer.running')
 page.evaluate('timer.deadline=Date.now()-1000')
 page.wait_for_timeout(1100)
 assert not page.evaluate('timer.running')
 assert page.evaluate('minutesAll()')>=1
 assert page.evaluate('state.activity[localDate()].types.focus')>=1
 print('PASS: editable focus duration, completed session and activity tracking')
 # Legacy backup migration
 migrated=page.evaluate('''() => normalizeState({version:1,days:{d2:{learned:true,steps:[true,true,true],quizPassed:true,completedAt:"2026-10-01T13:00:00Z",notes:"legacy"}},projects:{}})''')
 assert migrated['version']==2
 assert migrated['days']['d2']['steps']==[True]*5
 assert migrated['days']['d2']['quizPassed']
 assert migrated['days']['d2']['notes']=='legacy'
 print('PASS: v1 progress migration to v2 schema')
 print('Page JS errors',errors)
 assert not errors,errors
 # Mobile independent browser instance
 mobile=ctx.new_page();mobile.set_viewport_size({'width':390,'height':844});mobile.on('pageerror',lambda e:errors.append(str(e)))
 mobile.set_content(html,wait_until='domcontentloaded');mobile.wait_for_selector('.hero')
 mobile.locator('[data-action="toggle-sidebar"]').click()
 assert 'open' in mobile.locator('#sidebar').get_attribute('class')
 mobile.locator('[data-action="nav"][data-route="labs"]').click()
 assert mobile.locator('.lab-tab').count()==32
 assert mobile.locator('.lab-toolbar .btn').first.is_visible()
 print('PASS: mobile navigation and lab layout')
 assert not errors,errors
 browser.close()
