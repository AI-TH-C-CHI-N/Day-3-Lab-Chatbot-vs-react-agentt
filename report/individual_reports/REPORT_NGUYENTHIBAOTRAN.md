# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyễn Thị Bảo Trân
- **Student ID**: 2A202600917
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Trong phan viec ca nhan, em da hoan thien phan test, telemetry, frontend/backend services va tai lieu minh hoa de project khop voi luong lam viec thuc te cua lab.

- **Modules Implemented**:
  - `tests/test_tools.py`: unit test tung tool rieng le, gom case input dung/sai cho `list_node_types`, `validate_spec`, `compile_spec`, `create_workflow`, `activate_workflow`, `get_workflow`, `delete_workflow`.
  - `tests/test_agent.py`: integration test cho ReActAgent, kiem tra tra `Final Answer` va gioi han `max_steps`.
  - `tests/test_metrics.py`: test `PerformanceTracker.summarize()` va `export_to_json()`.
  - `src/telemetry/metrics.py`: them `summarize()` va `export_to_json()` de tong hop latency, tokens, cost.
  - `services/backend/app.py`: backend HTTP phuc vu web demo, noi truc tiep voi runtime trong `src/`.
  - `services/frontend/index.html`, `services/frontend/chat.html`, `services/frontend/styles.css`: chuyen giao dien tu project travel planner sang Chatbot vs ReAct Agent lab.
  - `report/flowchart.md`, `report/assets/react_loop.png`, `report/assets/architecture.png`: tach flowchart ra ảnh PNG de ro rang hon.
  - `report/usecases/*.md` va `report/appendix/*.md`: tach use case, telemetry, provider switching, ablation, production readiness thanh file rieng.
  - `README.md`: cap nhat huong dan chay `python main.py`, mo ta use case va danh sach tool.
  - `src/core/provider_factory.py`: provider switching giua OpenAI / Gemini / Local.
  - `src/agent/baseline_chatbot.py` va `src/agent/chatbot.py`: giu hai che do baseline vs ReAct de so sanh truc tiep.

- **Code Highlights**:
  - **Test suite theo contract**:
    - `tests/test_tools.py` bao phu tung tool rieng le, gom ca `error:` path va `ok | ...` path.
    - `tests/test_agent.py` kiem tra agent co tra ve `Final Answer` va co dung khi vuot `max_steps`.
  - **Telemetry pipeline**:
    - `src/telemetry/metrics.py` gom metrics trong `session_metrics`, sau do `summarize()` tra ve avg latency, total tokens, total cost.
    - `export_to_json()` cho phep xuat report ra file JSON de dung trong dashboard/report.
  - **Frontend/backend services**:
    - `services/backend/app.py` phuc vu static frontend va endpoint `/api/chat`, `/api/health`, `/api/metrics`.
    - `services/frontend/index.html` va `chat.html` duoc doi branding sang Chatbot vs ReAct Agent lab.
    - `services/frontend/styles.css` duoc tinh chinh mau sac, layout va mode selector de demo ro hon.
  - **Flowchart va use case**:
    - `report/flowchart.md` chi lien ket den 2 PNG chart: React loop va overall architecture.
    - `report/usecases/` tach 8 trace/use case rieng, `report/appendix/` tach telemetry, provider switching, ablation va production readiness.
  - **Provider switching**:
    - `src/core/provider_factory.py` dung fallback order de de chay tren OpenAI, Gemini hoac Local.
    - `report/appendix/provider_switching.md` tong hop trade-off giua do chinh xac, toc do va chi phi.

- **Documentation (interaction with ReAct loop)**:
  - ReAct loop van giu contract string in/string out (`Action: tool(args)` -> `Observation: ok|error`).
  - Phan web demo va phan test deu dung cung code runtime trong `src/`, nen khong co sai lech giua code chay thuc va code mo ta trong report.
  - Tai lieu da duoc tach thanh cac file nho de de review: flowchart, use case, appendix va services demo.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**:
  - Ban dau web demo khong khop project vi `services/` van con giao dien Travel Planner va backend chua noi dung theo runtime moi.
  - Agent co the lap lai loi tich hop (vi du activation/config) nhieu lan, ton step budget ma khong tao gia tri moi.
  - Ngoai ra, parser `Action:` dung regex don gian de vo khi output LLM co dau ngoac phuc tap.

- **Log Source**:
  - `logs/2026-06-01.log`
  - `debug.md`
  - Trich su kien thuc te:
    - `TOOL_CALL` voi `list_node_types` tra ve `ok | ...`
    - `create_workflow` thanh cong, nhung `activate_workflow` that bai lap lai voi `Bad request: Could not find property option`.
    - Backend smoke test qua `services/backend/app.py` va `/api/health` xac nhan service da chay dung sau khi update.

- **Diagnosis**:
  - Loi khong nam o mot tool rieng le ma o su ket hop giua:
    - parser action chua du robust,
    - vong lap agent chua co co che cat som khi gap loi lap lai,
    - rang buoc runtime n8n (activation) phuc tap hon validate cau truc,
    - services backend/frontend ban dau khong khop voi code base `src/` nen can dong bo lai.

- **Solution**:
  1. Them `_parse_action(...)` dung bo dem ngoac + xu ly quote/escape de parse on dinh hon regex cu.
  2. Them co che "repeated error guard": neu cung mot `error:` lap lai >= 2 lan lien tiep thi dung loop som va tra loi huong dan.
 3. Tach provider factory de giam loi khoi tao model va de fallback thong minh hon.
 4. Them `summarize()` va `export_to_json()` trong telemetry de co du lieu tong hop.
 5. Dong bo lai backend/frontend trong `services/` de web demo chay dung cung project hien tai.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**:
  - Chatbot thuong (`src/agent/baseline_chatbot.py`) phan hoi nhanh, gon cho cau hoi don gian.
  - ReAct Agent (`src/agent/chatbot.py`) manh hon ro o bai toan da buoc vi biet goi tool, validate, compile, va tao workflow that.
  - Khi chay web demo, em thay ro su khac biet giua 2 mode ngay tren frontend: baseline tra loi truc tiep, con agent co trace suy luan.

2. **Reliability**:
   - Agent co the kem hon chatbot trong cac cau hoi khong can tool (ton them step/tokens).
   - Tuy nhien sau nang cap parser + repeated-error guard, agent ben hon trong tinh huong output phuc tap hoac loi tich hop lap lai.
  - Provider switching giup giam nguy co phai fix theo tung model rieng le, nen demo va test on dinh hon.

3. **Observation**:
   - Observation la diem khac biet cot loi: ket qua `ok | ...` / `error: ...` tu moi tool giup step sau dieu chinh quyet dinh.
   - Khong co Observation, he thong chi la chatbot mo ta, khong phai agent hanh dong.
  - Trong report nay em tach use case/appendix ra rieng, nen observe duoc ca trace thanh cong va trace loi mot cach ro rang hon.

---

## IV. Future Improvements (5 Points)

- **Scalability**:
  - Bo sung bo nho ngan gon transcript (summary window) de session dai khong vuot context.
  - Tach orchestration thanh state machine (vi du graph-based) khi so tool tang.
  - Tiep tuc tach frontend JS ra file rieng neu can them tinh nang metrics dashboard.

- **Safety**:
  - Them preflight checker truoc cac tool co side effect (`create`, `activate`, `delete`).
  - Them allowlist schema-level cho tung node kind de giam loi runtime activation.
  - Them smoke test cho `/api/chat` va `/api/health` trong services backend.

- **Performance**:
  - Chon tool context theo nguyen tac retrieval (chi dua tool lien quan vao prompt moi step).
  - Them timeout/retry policy co phan loai loi de giam thoi gian cho case that bai lap lai.
  - Dung report metrics JSON de doi chieu latency, token va cost giua cac provider.

---

## V. Files I Personally Worked On

- [tests/test_tools.py](../../tests/test_tools.py)
- [tests/test_agent.py](../../tests/test_agent.py)
- [tests/test_metrics.py](../../tests/test_metrics.py)
- [src/telemetry/metrics.py](../../src/telemetry/metrics.py)
- [services/backend/app.py](../../services/backend/app.py)
- [services/frontend/index.html](../../services/frontend/index.html)
- [services/frontend/chat.html](../../services/frontend/chat.html)
- [services/frontend/styles.css](../../services/frontend/styles.css)
- [report/flowchart.md](../flowchart.md)
- [report/usecases/README.md](../usecases/README.md)
- [report/appendix/telemetry_dashboard.md](../appendix/telemetry_dashboard.md)
- [report/appendix/provider_switching.md](../appendix/provider_switching.md)

> [!NOTE]
> File da duoc cap nhat theo template ca nhan va phan anh dung nhung phan em da lam trong project, gom ca tests, telemetry, services va tai lieu.
