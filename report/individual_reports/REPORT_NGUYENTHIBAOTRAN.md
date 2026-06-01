# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Nguyễn Thị Bảo Trân
- **Student ID**: 2A202600917
- **Date**: 2026-06-01

---

## I. Technical Contribution (15 Points)

Trong phan viec ca nhan, em da bo sung day du 2 phien ban theo dung muc tieu lab (Chatbot vs ReAct Agent) va nang cap agent de thong minh, ben hon khi van hanh.

- **Modules Implemented**:
  - `src/agent/baseline_chatbot.py` (them moi): chatbot baseline theo dung yeu cau lab, khong dung tools/ReAct.
  - `src/core/provider_factory.py` (them moi): khoi tao LLM linh hoat theo `.env` va fallback giua OpenAI/Gemini/Local.
  - `src/agent/chatbot.py` (cap nhat): bo hard-code OpenAI, dung provider factory.
  - `src/agent/agent.py` (cap nhat): parse `Action:` robust hon va chan vong lap khi cung loi tool lap lai.
  - `README.md` (cap nhat): bo sung huong dan chay 2 phien ban de so sanh truc tiep.

- **Code Highlights**:
  - **Bo sung 2 ban dung yeu cau**:
    - Chatbot thuong: `src/agent/baseline_chatbot.py`
    - ReAct Agent: `src/agent/chatbot.py`
  - **Nang cap parser thong minh hon trong ReAct loop** (`src/agent/agent.py`):
    - Them ham `_parse_action(...)` de parse duoc args da dong, co nested parentheses va chuoi quote.
    - Giam fail do regex don gian khi output LLM phuc tap.
  - **Tranh loop vo ich khi gap cung mot loi** (`src/agent/agent.py`):
    - Neu `observation` bat dau bang `error:` va lap lai lien tiep, agent dung som va tra thong bao huong dan nguoi dung.
  - **Provider linh hoat, de failover** (`src/core/provider_factory.py`):
    - Doc `DEFAULT_PROVIDER`, fallback sang provider kha dung tiep theo neu provider uu tien khong san sang.
    - Giam nguy co "khong chay duoc" do thieu 1 loai API key.

- **Documentation (interaction with ReAct loop)**:
  - ReAct loop van giu contract string in/string out (`Action: tool(args)` -> `Observation: ok|error`).
  - Cac nang cap moi khong thay doi giao dien tool, chi tang do ben:
    - parser Action on dinh hon,
    - stop condition thong minh hon khi tool loi lap lai,
    - provider init thong minh hon o layer runtime.

---

## II. Debugging Case Study (10 Points)

- **Problem Description**:
  - Agent co the lap lai loi tich hop (vi du activation/config) nhieu lan, ton step budget ma khong tao gia tri moi.
  - Ngoai ra, parser `Action:` dung regex don gian de vo khi output LLM co dau ngoac phuc tap.

- **Log Source**:
  - `logs/2026-06-01.log`
  - Trich su kien thuc te:
    - `TOOL_CALL` voi `list_node_types` tra ve `ok | ...`
    - Sau do `AGENT_STEP` cho thay model tiep tuc suy luan them nhung co the khong tien den action hieu qua trong cac case loi tich hop.
  - `debug.md` cung cho thay class loi tich hop: `activate_workflow` that bai lap lai voi `Bad request: Could not find property option`.

- **Diagnosis**:
  - Loi khong nam o mot tool rieng le ma o su ket hop giua:
    - parser action chua du robust,
    - vong lap agent chua co co che cat som khi gap loi lap lai,
    - rang buoc runtime n8n (activation) phuc tap hon validate cau truc.

- **Solution**:
  1. Them `_parse_action(...)` dung bo dem ngoac + xu ly quote/escape de parse on dinh hon regex cu.
  2. Them co che "repeated error guard": neu cung mot `error:` lap lai >= 2 lan lien tiep thi dung loop som va tra loi huong dan.
  3. Tach provider factory de giam loi khoi tao model va de fallback thong minh.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**:
  - Chatbot thuong (`src/agent/baseline_chatbot.py`) phan hoi nhanh, gon cho cau hoi don gian.
   - ReAct Agent (`src/agent/chatbot.py`) manh hon ro o bai toan da buoc vi biet goi tool, validate, compile, va tao workflow that.

2. **Reliability**:
   - Agent co the kem hon chatbot trong cac cau hoi khong can tool (ton them step/tokens).
   - Tuy nhien sau nang cap parser + repeated-error guard, agent ben hon trong tinh huong output phuc tap hoac loi tich hop lap lai.

3. **Observation**:
   - Observation la diem khac biet cot loi: ket qua `ok | ...` / `error: ...` tu moi tool giup step sau dieu chinh quyet dinh.
   - Khong co Observation, he thong chi la chatbot mo ta, khong phai agent hanh dong.

---

## IV. Future Improvements (5 Points)

- **Scalability**:
  - Bo sung bo nho ngan gon transcript (summary window) de session dai khong vuot context.
  - Tach orchestration thanh state machine (vi du graph-based) khi so tool tang.

- **Safety**:
  - Them preflight checker truoc cac tool co side effect (`create`, `activate`, `delete`).
  - Them allowlist schema-level cho tung node kind de giam loi runtime activation.

- **Performance**:
  - Chon tool context theo nguyen tac retrieval (chi dua tool lien quan vao prompt moi step).
  - Them timeout/retry policy co phan loai loi de giam thoi gian cho case that bai lap lai.

---

> [!NOTE]
> File da duoc cap nhat theo template ca nhan va phan anh dung thay doi thuc te trong project.
