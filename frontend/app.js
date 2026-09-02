const state = {
  levels: [],
  sentenceLibrary: [],
  activeLibraryCategory: "polite-questions",
  activeLevelId: "everyday",
  level: null,
  scenario: null,
  scenarioIndex: 0,
  history: [],
  lastPartnerReply: "",
  completed: false,
  recognition: null,
  englishOnly: false,
  pronunciationSample: "",
  reviewIndex: 0,
  reviewFilter: "all",
  reviewCurrentId: null,
  challengePromptIndex: 0,
  challengeSeconds: 60,
  challengeInterval: null,
  challengeRecognition: null,
  challengeTranscript: "",
  challengeRunning: false,
  authUser: null,
  authMode: "login",
  syncTimer: null,
  csrfToken: null,
  sessions: [],
  sessionId: null,
  activeHistoryId: null,
};

const storeKey = "talkmate-progress-v1";
const deviceKey = "talkmate-device-id-v1";
const challengePrompts = [
  "Tell me about a place you would love to visit and why.",
  "Describe the best meal you have had recently.",
  "Talk about a small win you had this week.",
  "Recommend a movie, book, or game to a friend.",
  "Imagine you are at an airport. What would you ask the staff?",
  "Tell a new colleague what you enjoy doing after work.",
];
const scoreLabels = {
  relevance: "relevance",
  grammar: "grammar",
  word_choice: "word choice",
  sentence: "sentence",
  naturalness: "naturalness",
  clarity: "clarity",
  confidence: "confidence",
};
const scoreHints = {
  relevance: "Does the answer match this situation?",
  grammar: "Are the grammar forms correct?",
  word_choice: "Are the words accurate and suitable?",
  sentence: "Is the sentence complete and well formed?",
  naturalness: "Does it sound natural and polite?",
  clarity: "Is the meaning easy to understand?",
  confidence: "Does the answer sound ready to use?",
};
const guardReasonLabels = {
  off_topic: "OFF TOPIC - does not match this scene",
  incomplete: "INCOMPLETE - write one complete sentence",
  repeated: "REPEATED - remove repeated words or phrases",
  keyword_soup: "KEYWORD SOUP - arrange the words into a sentence",
  profanity: "PROFANITY - keep practice respectful",
  language: "LANGUAGE - answer in English for this scene",
};
const reviewCategoryMeta = {
  articles: { label: "ARTICLES", name: "Mạo từ", hint: "a / an / the" },
  prepositions: { label: "PREPOSITIONS", name: "Giới từ", hint: "in / on / at / to" },
  verb_forms: { label: "VERB FORMS", name: "Chia động từ", hint: "have / has / did / can" },
  word_order: { label: "WORD ORDER", name: "Trật tự câu", hint: "question and sentence structure" },
  word_choice: { label: "WORD CHOICE", name: "Cách dùng từ", hint: "natural phrases" },
};
const reviewExercisePrompts = {
  articles: "Add the correct article before the singular noun.",
  prepositions: "Choose the preposition that makes the phrase natural.",
  verb_forms: "Fix the verb form to match the subject or tense.",
  word_order: "Put the words in a natural English order.",
  word_choice: "Rewrite this with a more natural English phrase.",
};
const badges = [
  { id: "first_scene", name: "FIRST HELLO", hint: "Complete one conversation." },
  { id: "five_minutes", name: "FIVE MINUTES", hint: "Speak for five minutes in one day." },
  { id: "brave_minute", name: "BRAVE MINUTE", hint: "Finish the 60-second challenge." },
  { id: "streak_three", name: "STEADY VOICE", hint: "Practice three days in a row." },
  { id: "xp_250", name: "ON A ROLL", hint: "Earn 250 XP." },
];
const $ = (selector) => document.querySelector(selector);
const els = {
  home: $("#home"),
  practice: $("#practice"),
  progress: $("#progress-view"),
  levels: $("#levels"),
  scenarios: $("#scenario-list"),
  libraryCount: $("#library-count"),
  libraryCategories: $("#library-categories"),
  libraryCards: $("#library-cards"),
  badge: $("#ai-badge"),
  lessonCount: $("#lesson-count"),
  title: $("#sc-title"),
  context: $("#sc-context"),
  goal: $("#sc-goal"),
  taskScore: $("#task-score"),
  taskProgress: $("#task-progress"),
  conversationGoals: $("#conversation-goals"),
  category: $("#sc-category"),
  icon: $("#scene-icon"),
  vocabulary: $("#vocabulary"),
  sentenceBuilder: $("#sentence-builder"),
  builderLabel: $("#builder-label"),
  builderHint: $("#builder-hint"),
  builderFrame: $("#builder-frame"),
  builderSlots: $("#builder-slots"),
  builderPreview: $("#builder-preview"),
  builderExamples: $("#builder-examples"),
  chat: $("#chat"),
  input: $("#input"),
  composer: $("#composer"),
  send: $("#btn-send"),
  coachBox: $("#coach-box"),
  feedback: $("#feedback"),
  guardReason: $("#guard-reason"),
  grammarNote: $("#grammar-note"),
  wordChoiceNote: $("#word-choice-note"),
  sentencePattern: $("#sentence-pattern"),
  improvedWrap: $("#improved-wrap"),
  improved: $("#improved"),
  tip: $("#tip"),
  pronunciationBox: $("#pronunciation-box"),
  pronunciationLabel: $("#pronunciation-label"),
  pronunciationScore: $("#pronunciation-score"),
  pronunciationHeard: $("#pronunciation-heard"),
  unclearWords: $("#unclear-words"),
  pronunciationTip: $("#pronunciation-tip"),
  scores: $("#scores"),
  score: $("#overall-score"),
  finished: $("#finished"),
  turnCounter: $("#turn-counter"),
  mode: $("#mode-label"),
  streak: $("#streak-count"),
  dailyProgress: $("#daily-progress"),
  dailyStatus: $("#daily-status"),
  todayLabel: $("#today-label"),
  statScenes: $("#stat-scenes"),
  statStreak: $("#stat-streak"),
  statScore: $("#stat-score"),
  nextStep: $("#next-step"),
  goalSelect: $("#goal-select"),
  focusSummary: $("#focus-summary"),
  englishOnly: $("#english-only"),
  sessionLanguage: $("#session-language"),
  levelSelect: $("#level-select"),
  reviewEmpty: $("#review-empty"),
  reviewCard: $("#review-card"),
  reviewCount: $("#review-count"),
  reviewDailyProgress: $("#review-daily-progress"),
  reviewDailyBar: $("#review-daily-bar"),
  reviewCategories: $("#review-categories"),
  reviewTag: $("#review-tag"),
  reviewInstruction: $("#review-instruction"),
  reviewMode: $("#review-mode"),
  reviewSource: $("#review-source"),
  reviewInput: $("#review-input"),
  reviewAnswer: $("#review-answer"),
  reviewCorrection: $("#review-correction"),
  reviewNote: $("#review-note"),
  xpTotal: $("#xp-total"),
  levelTotal: $("#level-total"),
  badgeTotal: $("#badge-total"),
  badgePreview: $("#badge-preview"),
  xpProgress: $("#xp-progress"),
  xpNext: $("#xp-next"),
  challenge: $("#challenge-view"),
  challengePrompt: $("#challenge-prompt"),
  challengeTimer: $("#challenge-timer"),
  challengeTranscript: $("#challenge-transcript"),
  challengeResult: $("#challenge-result"),
  challengeResultTitle: $("#challenge-result-title"),
  challengeResultCopy: $("#challenge-result-copy"),
  challengeStart: $("#btn-start-challenge"),
  challengeStop: $("#btn-stop-challenge"),
  badgeList: $("#badge-list"),
  badgeProgress: $("#badge-progress"),
  weeklyChart: $("#weekly-chart"),
  weeklyCaption: $("#weekly-caption"),
  syncStatus: $("#sync-status"),
  sessionHistory: $("#session-history"),
  historyCount: $("#history-count"),
  historyEmpty: $("#history-empty"),
  account: $("#btn-account"),
  authModal: $("#auth-modal"),
  authTitle: $("#auth-title"),
  authForm: $("#auth-form"),
  authName: $("#auth-name"),
  authEmail: $("#auth-email"),
  authPassword: $("#auth-password"),
  authError: $("#auth-error"),
  authNameField: $("#name-field"),
  authLoginTab: $("#auth-login-tab"),
  authRegisterTab: $("#auth-register-tab"),
  historyModal: $("#history-modal"),
  historyTitle: $("#history-title"),
  historyMeta: $("#history-meta"),
  historyTranscript: $("#history-transcript"),
};

function getProgress() {
  try {
    const saved = JSON.parse(localStorage.getItem(storeKey)) || {};
    const review = saved.review && typeof saved.review === "object" ? saved.review : {};
    return {
      ...saved,
      completed: Array.isArray(saved.completed) ? saved.completed : [],
      scores: Array.isArray(saved.scores) ? saved.scores : [],
      activeDays: Array.isArray(saved.activeDays) ? saved.activeDays : [],
      scoreEvents: Array.isArray(saved.scoreEvents) ? saved.scoreEvents : [],
      reviewItems: Array.isArray(saved.reviewItems) ? saved.reviewItems : [],
      review: {
        dailyCompleted: review.dailyCompleted && typeof review.dailyCompleted === "object" ? review.dailyCompleted : {},
        sessions: Number(review.sessions) || 0,
        attempts: Number(review.attempts) || 0,
        correct: Number(review.correct) || 0,
      },
    };
  } catch {
    return { completed: [], scores: [], activeDays: [], reviewItems: [], review: { dailyCompleted: {}, sessions: 0, attempts: 0, correct: 0 } };
  }
}

function ensureReviewStats(progress) {
  progress.review ||= { dailyCompleted: {}, sessions: 0, attempts: 0, correct: 0 };
  progress.review.dailyCompleted ||= {};
  progress.review.sessions = Number(progress.review.sessions) || 0;
  progress.review.attempts = Number(progress.review.attempts) || 0;
  progress.review.correct = Number(progress.review.correct) || 0;
  return progress.review;
}

function saveProgress(progress) {
  localStorage.setItem(storeKey, JSON.stringify(progressWithMetadata(progress)));
  queueSync(progress);
}

function progressWithMetadata(progress) {
  return { ...progress };
}

function eventId(prefix) {
  return `${prefix}-${Date.now()}-${crypto.randomUUID?.() || Math.random().toString(36).slice(2)}`;
}

function deviceId() {
  let id = localStorage.getItem(deviceKey);
  if (!id) {
    id = eventId("device");
    localStorage.setItem(deviceKey, id);
  }
  return id;
}

function syncHeaders() {
  return { "Content-Type": "application/json", "X-CSRF-Token": state.csrfToken || "" };
}

function queueSync(progress) {
  if (!state.authUser) return;
  window.clearTimeout(state.syncTimer);
  state.syncTimer = window.setTimeout(() => syncProgress(progress), 700);
}

async function syncProgress(progress = getProgress()) {
  if (!state.authUser) return;
  try {
    const response = await fetch("/api/sync", {
      method: "POST",
      headers: syncHeaders(),
      body: JSON.stringify({ progress }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Sync unavailable");
    if (data.csrf_token) state.csrfToken = data.csrf_token;
    if (data.progress) {
      localStorage.setItem(storeKey, JSON.stringify(data.progress));
      updateProgressUI();
    }
    els.syncStatus.textContent = "Synced across devices";
  } catch {
    els.syncStatus.textContent = "Sync will retry when online";
  }
}

function ensureMomentum(progress) {
  progress.momentum ||= { xp: 0, xpEvents: [], badges: [], dailyMinutes: {}, challenges: 0, challengeEvents: [] };
  progress.momentum.badges ||= [];
  progress.momentum.dailyMinutes ||= {};
  progress.momentum.xp ||= 0;
  progress.momentum.xpEvents ||= progress.momentum.xp ? [{ id: "legacy-xp", amount: progress.momentum.xp, at: "" }] : [];
  progress.momentum.challenges ||= 0;
  progress.momentum.challengeEvents ||= progress.momentum.challenges ? [{ id: "legacy-challenges", amount: progress.momentum.challenges, at: "" }] : [];
  progress.momentum.xp = progress.momentum.xpEvents.reduce((total, event) => total + Number(event.amount || 0), 0);
  progress.momentum.challenges = progress.momentum.challengeEvents.reduce((total, event) => total + Number(event.amount || 0), 0);
  return progress.momentum;
}

function levelFromXp(xp) {
  return Math.floor(xp / 100) + 1;
}

function xpForCurrentLevel(xp) {
  return xp % 100;
}

function awardXp(amount) {
  const progress = getProgress();
  const momentum = ensureMomentum(progress);
  momentum.xpEvents.push({ id: eventId("xp"), amount, at: new Date().toISOString() });
  momentum.xp += amount;
  evaluateBadges(progress);
  saveProgress(progress);
  updateProgressUI();
}

function evaluateBadges(progress) {
  const momentum = ensureMomentum(progress);
  const currentStreak = getStreak(progress.activeDays || []);
  const todayMinutes = momentum.dailyMinutes[dayStamp()] || 0;
  const rules = {
    first_scene: (progress.completed || []).length >= 1,
    five_minutes: todayMinutes >= 5,
    brave_minute: momentum.challenges >= 1,
    streak_three: currentStreak >= 3,
    xp_250: momentum.xp >= 250,
  };
  badges.forEach((badge) => {
    if (rules[badge.id] && !momentum.badges.includes(badge.id)) momentum.badges.push(badge.id);
  });
}

function addDailyMinutes(minutes) {
  const progress = getProgress();
  const momentum = ensureMomentum(progress);
  const today = dayStamp();
  momentum.dailyMinutes[today] = Math.min(5, (momentum.dailyMinutes[today] || 0) + minutes);
  if (!progress.activeDays.includes(today)) progress.activeDays.push(today);
  evaluateBadges(progress);
  saveProgress(progress);
  updateProgressUI();
}

function getLearnerProfile() {
  const progress = getProgress();
  const profile = progress.profile || {};
  return {
    goal: profile.goal || "Speak more naturally in everyday conversations.",
    proficiency: profile.proficiency || "A2",
    target: profile.target || "travel",
    englishOnly: Boolean(profile.englishOnly),
    errors: profile.errors || {},
    strengths: profile.strengths || {},
  };
}

function learnerForCoach() {
  const profile = getLearnerProfile();
  const topItems = (items) => Object.entries(items)
    .sort(([, first], [, second]) => second - first)
    .slice(0, 3)
    .map(([name]) => name);
  return {
    goal: profile.goal,
    proficiency: profile.proficiency,
    target: profile.target,
    recurring_errors: topItems(profile.errors),
    strengths: topItems(profile.strengths),
  };
}

function updateProfile(mutator) {
  const progress = getProgress();
  progress.profile ||= { goal: "Speak more naturally in everyday conversations.", proficiency: "A2", target: "travel", englishOnly: false, errors: {}, strengths: {} };
  progress.profile.errors ||= {};
  progress.profile.strengths ||= {};
  mutator(progress.profile);
  progress.profile_updated_at = new Date().toISOString();
  saveProgress(progress);
  renderProfileUI();
}

function renderProfileUI() {
  const profile = getLearnerProfile();
  // Migrate the free-text goal from the previous version to the new target picker.
  const legacyGoal = profile.goal;
  const target = ["travel", "interview", "work", "dating"].includes(profile.target) ? profile.target : "travel";
  const targetNames = { travel: "Travel", interview: "Interview", work: "Work", dating: "Dating" };
  els.levelSelect.value = profile.proficiency;
  els.goalSelect.value = target;
  els.focusSummary.textContent = `${profile.proficiency} - ${targetNames[target]}`;
  if (legacyGoal && !profile.target) updateProfile((next) => { next.target = "travel"; next.goal = legacyGoal; });
  els.englishOnly.checked = profile.englishOnly;
}

function difficultyForLevel(level) {
  return level === "A1" ? "de" : ["B2", "C1"].includes(level) ? "kho" : "vua";
}

function updateLearningMemory(message, data) {
  const lower = message.toLowerCase();
  const patterns = [];
  if (data.improved && data.improved.trim().toLowerCase() !== lower.trim()) {
    patterns.push(reviewCategoryFor(message, data));
  }
  if (/\bi want\b/.test(lower)) patterns.push("polite requests");
  if (/\bi am agree\b/.test(lower)) patterns.push("verb forms after I");
  if (/\bi very like\b/.test(lower)) patterns.push("natural adverbs");
  if (/\bcan you to\b/.test(lower)) patterns.push("modal verbs");
  if (message.trim().split(/\s+/).length < 4) patterns.push("longer responses");
  const strengths = [];
  if ((data.scores?.naturalness || 0) >= 8) strengths.push("natural phrasing");
  if ((data.scores?.confidence || 0) >= 8) strengths.push("confident tone");
  if (/\?|could|would|what|how|where|when|why/i.test(message)) strengths.push("keeping a conversation going");
  updateProfile((profile) => {
    patterns.forEach((pattern) => { profile.errors[pattern] = (profile.errors[pattern] || 0) + 1; });
    strengths.forEach((strength) => { profile.strengths[strength] = (profile.strengths[strength] || 0) + 1; });
  });
}

function dayStamp(date = new Date()) {
  return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
}

function getStreak(days) {
  const dates = new Set(days || []);
  let streak = 0;
  const cursor = new Date();
  while (dates.has(dayStamp(cursor))) {
    streak += 1;
    cursor.setDate(cursor.getDate() - 1);
  }
  return streak;
}

function updateProgressUI() {
  const progress = getProgress();
  const momentum = ensureMomentum(progress);
  const streak = getStreak(progress.activeDays);
  const todayMinutes = momentum.dailyMinutes[dayStamp()] || 0;
  const todayDone = todayMinutes >= 5;
  els.streak.textContent = `${streak}-day`;
  els.dailyProgress.style.width = `${Math.min(100, todayMinutes * 20)}%`;
  els.dailyStatus.textContent = `${todayMinutes} / 5 minutes`;
  els.todayLabel.textContent = todayDone ? "Daily mission complete" : `${Math.max(0, 5 - todayMinutes)} minutes to today's win`;
  els.statScenes.textContent = progress.completed.length;
  els.statStreak.textContent = `${streak} ${streak === 1 ? "day" : "days"}`;
  const average = progress.scores.length
    ? (progress.scores.reduce((sum, item) => sum + item, 0) / progress.scores.length).toFixed(1)
    : "--";
  els.statScore.textContent = average;
  if (progress.completed.length) {
    els.nextStep.textContent = "Nice consistency. Pick a new scene and try one longer, more specific answer.";
  }
  const level = levelFromXp(momentum.xp);
  const currentXp = xpForCurrentLevel(momentum.xp);
  const latestBadge = badges.find((badge) => momentum.badges.includes(badge.id));
  els.xpTotal.textContent = momentum.xp;
  els.levelTotal.textContent = level;
  els.badgeTotal.textContent = momentum.badges.length;
  els.badgePreview.textContent = latestBadge?.name || "NEXT: FIRST HELLO";
  els.xpProgress.style.width = `${currentXp}%`;
  els.xpNext.textContent = `${100 - currentXp || 100} XP to Level ${level + 1}`;
  renderBadges();
  renderWeeklyChart(progress);
  renderReviewLab();
}

function renderWeeklyChart(progress = getProgress()) {
  if (!els.weeklyChart) return;
  const today = new Date();
  const days = Array.from({ length: 7 }, (_, index) => {
    const date = new Date(today);
    date.setDate(today.getDate() - (6 - index));
    return { date, stamp: dayStamp(date) };
  });
  const momentum = ensureMomentum(progress);
  const values = days.map(({ stamp }) => Math.min(5, momentum.dailyMinutes[stamp] || 0));
  const labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  els.weeklyChart.replaceChildren();
  days.forEach(({ date, stamp }, index) => {
    const column = document.createElement("div");
    column.className = "day-column";
    column.innerHTML = `<div class="day-bar-wrap"><div class="day-bar${values[index] ? " active" : ""}" style="height:${Math.max(4, values[index] * 20)}%"></div></div><span class="day-label">${labels[date.getDay()]}</span>`;
    els.weeklyChart.append(column);
  });
  els.weeklyCaption.textContent = state.authUser ? "Your activity is synced to your TalkMate account." : "Sign in to sync this chart across devices.";
}

function formatSessionDate(value) {
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? "Saved conversation" : date.toLocaleString();
}

function renderSessionHistory() {
  if (!els.sessionHistory) return;
  els.sessionHistory.replaceChildren();
  const sessions = state.sessions || [];
  els.historyCount.textContent = state.authUser
    ? `${sessions.length} saved session${sessions.length === 1 ? "" : "s"}`
    : "Sign in to save sessions";
  if (!sessions.length) {
    const empty = document.createElement("p");
    empty.className = "review-empty";
    empty.textContent = state.authUser
      ? "Finish a scene to keep its full conversation here."
      : "Sign in and complete a scene to keep your conversation history here.";
    els.sessionHistory.append(empty);
    return;
  }
  sessions.forEach((session) => {
    const item = document.createElement("button");
    item.className = "session-item";
    item.type = "button";
    const title = document.createElement("strong");
    title.textContent = session.title || "TalkMate session";
    const details = document.createElement("span");
    const turns = Number(session.turns || 0);
    const score = Number(session.overall);
    details.textContent = `${formatSessionDate(session.completed_at || session.created_at)} · ${turns} turns${Number.isFinite(score) ? ` · ${score}/10` : ""}`;
    item.append(title, details);
    item.addEventListener("click", () => openSessionHistory(session));
    els.sessionHistory.append(item);
  });
}

function openSessionHistory(savedSession) {
  els.historyTitle.textContent = savedSession.title || "TalkMate session";
  els.historyMeta.textContent = `${formatSessionDate(savedSession.completed_at || savedSession.created_at)} · ${savedSession.level || "A2"} · ${savedSession.turns || 0} turns`;
  els.historyTranscript.replaceChildren();
  const transcript = Array.isArray(savedSession.transcript) ? savedSession.transcript : [];
  if (!transcript.length) {
    const note = document.createElement("p");
    note.textContent = "This older session was saved without a transcript.";
    els.historyTranscript.append(note);
  } else {
    transcript.forEach((turn) => {
      const item = document.createElement("article");
      item.className = `history-turn ${turn.role === "user" ? "user" : "partner"}`;
      const label = document.createElement("span");
      label.textContent = turn.role === "user" ? "YOU" : "YOUR PARTNER";
      const text = document.createElement("p");
      text.textContent = turn.text || "";
      item.append(label, text);
      els.historyTranscript.append(item);
    });
  }
  els.historyModal.classList.remove("hidden");
}

function closeSessionHistory() {
  els.historyModal.classList.add("hidden");
}

function iconText(icon) {
  return { cup: "cafe", map: "map", home: "home", phone: "call", doctor: "care", key: "rent", plate: "dish", globe: "world", briefcase: "work", spark: "idea", handshake: "meet", presentation: "pitch" }[icon] || "talk";
}

function showView(view) {
  if (view !== "challenge" && state.challengeRunning) finishChallenge(false);
  els.home.classList.toggle("hidden", view !== "home");
  els.practice.classList.toggle("hidden", view !== "practice");
  els.progress.classList.toggle("hidden", view !== "progress");
  els.challenge.classList.toggle("hidden", view !== "challenge");
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function renderLevels() {
  els.levels.replaceChildren();
  state.levels.forEach((level) => {
    const button = document.createElement("button");
    button.className = `level-tab${level.id === state.activeLevelId ? " active" : ""}`;
    button.textContent = level.name;
    button.addEventListener("click", () => {
      state.activeLevelId = level.id;
      renderLevels();
      renderScenarios();
    });
    els.levels.append(button);
  });
}

async function copyLibraryText(text, button) {
  try {
    await navigator.clipboard.writeText(text);
    const original = button.textContent;
    button.textContent = "Copied";
    window.setTimeout(() => { button.textContent = original; }, 1200);
  } catch {
    button.textContent = "Select & copy";
  }
}

function renderSentenceLibrary(categoryId = state.activeLibraryCategory) {
  const categories = Array.isArray(state.sentenceLibrary) ? state.sentenceLibrary : [];
  if (!els.libraryCategories || !els.libraryCards) return;
  els.libraryCategories.replaceChildren();
  els.libraryCards.replaceChildren();
  if (!categories.length) {
    els.libraryCount.textContent = "Offline phrase bank";
    const empty = document.createElement("p");
    empty.className = "library-empty";
    empty.textContent = "Phrase library is loading...";
    els.libraryCards.append(empty);
    return;
  }
  const active = categories.find((category) => category.id === categoryId) || categories[0];
  state.activeLibraryCategory = active.id;
  const itemCount = categories.reduce((total, category) => total + (category.items || []).length, 0);
  els.libraryCount.textContent = `${itemCount} useful patterns`;

  categories.forEach((category) => {
    const tab = document.createElement("button");
    tab.className = `library-tab${category.id === active.id ? " active" : ""}`;
    tab.type = "button";
    tab.setAttribute("role", "tab");
    tab.setAttribute("aria-selected", category.id === active.id ? "true" : "false");
    tab.textContent = category.label;
    tab.addEventListener("click", () => renderSentenceLibrary(category.id));
    els.libraryCategories.append(tab);
  });

  (active.items || []).forEach((item) => {
    const card = document.createElement("article");
    card.className = "library-card";
    const title = document.createElement("h3");
    title.textContent = item.title;
    const structureLabel = document.createElement("span");
    structureLabel.className = "library-label";
    structureLabel.textContent = "STRUCTURE";
    const structure = document.createElement("p");
    structure.className = "library-structure";
    structure.textContent = item.structure;
    const whenLabel = document.createElement("span");
    whenLabel.className = "library-label";
    whenLabel.textContent = "WHEN TO USE IT";
    const when = document.createElement("p");
    when.className = "library-when";
    when.textContent = item.when;
    const variantsLabel = document.createElement("span");
    variantsLabel.className = "library-label";
    variantsLabel.textContent = "NATURAL VARIATIONS";
    const variants = document.createElement("div");
    variants.className = "library-variants";
    (item.examples || []).forEach((example) => {
      const row = document.createElement("div");
      row.className = "library-example";
      const text = document.createElement("span");
      text.textContent = example;
      const copy = document.createElement("button");
      copy.type = "button";
      copy.className = "library-copy";
      copy.textContent = "Copy";
      copy.title = "Copy this example";
      copy.addEventListener("click", () => copyLibraryText(example, copy));
      row.append(text, copy);
      variants.append(row);
    });
    card.append(title, structureLabel, structure, whenLabel, when, variantsLabel, variants);
    els.libraryCards.append(card);
  });
}

function getActiveLevel() {
  return state.levels.find((level) => level.id === state.activeLevelId) || state.levels[0];
}

async function startScenario(index) {
  const level = getActiveLevel();
  if (!level) return;
  const response = await fetch("/api/start", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level: level.id, scenario_index: index }),
  });
  if (!response.ok) throw new Error("Could not start this scene.");
  const data = await response.json();
  state.level = data.level;
  state.scenario = data.scenario;
  state.scenarioIndex = data.scenario_index;
  state.history = [];
  state.lastPartnerReply = data.opening;
  state.completed = false;
  state.sessionStartedAt = Date.now();
  state.sessionId = eventId("session");
  state.englishOnly = getLearnerProfile().englishOnly;
  renderPractice(data.opening);
  showView("practice");
  speak(data.opening);
}

function renderBadges() {
  const progress = getProgress();
  const momentum = ensureMomentum(progress);
  els.badgeList.replaceChildren();
  badges.forEach((badge, index) => {
    const unlocked = momentum.badges.includes(badge.id);
    const item = document.createElement("article");
    item.className = `badge-item${unlocked ? "" : " locked"}`;
    item.innerHTML = `<span class="badge-seal">${unlocked ? "*" : index + 1}</span><strong>${badge.name}</strong><p>${badge.hint}</p>`;
    els.badgeList.append(item);
  });
  els.badgeProgress.textContent = `${momentum.badges.length} / ${badges.length} unlocked`;
}

function setAuthMode(mode) {
  state.authMode = mode;
  const registering = mode === "register";
  els.authTitle.textContent = registering ? "Make your progress portable." : "Keep your progress with you.";
  els.authNameField.classList.toggle("hidden", !registering);
  els.authLoginTab.classList.toggle("active", !registering);
  els.authRegisterTab.classList.toggle("active", registering);
  els.authPassword.autocomplete = registering ? "new-password" : "current-password";
  els.authError.textContent = "";
}

function openAuth() {
  els.authModal.classList.remove("hidden");
  setAuthMode(state.authMode);
  els.authEmail.focus();
}

function closeAuth() {
  els.authModal.classList.add("hidden");
  els.authForm.reset();
  els.authError.textContent = "";
}

async function loadAccount() {
  try {
    const response = await fetch("/api/auth/me");
    const data = await response.json();
    state.authUser = data.user || null;
    state.csrfToken = data.csrf_token || null;
  updateAccountUI();
  renderSessionHistory();
  if (state.authUser) {
      const sync = await fetch("/api/sync");
      if (sync.ok) {
        const remote = await sync.json();
        state.sessions = Array.isArray(remote.sessions) ? remote.sessions : [];
        renderSessionHistory();
        if (remote.progress) await syncProgress(getProgress());
      }
    }
  } catch {
    state.authUser = null;
    updateAccountUI();
  }
}

function updateAccountUI() {
  els.account.textContent = state.authUser ? state.authUser.name : "Sign in";
  els.account.classList.toggle("signed-in", Boolean(state.authUser));
  if (els.syncStatus) els.syncStatus.textContent = state.authUser ? "Synced across devices" : "Local progress";
  renderWeeklyChart();
}

async function submitAuth(event) {
  event.preventDefault();
  const registering = state.authMode === "register";
  const endpoint = registering ? "/api/auth/register" : "/api/auth/login";
  const body = { email: els.authEmail.value.trim(), password: els.authPassword.value };
  if (registering) body.name = els.authName.value.trim();
  const submit = els.authForm.querySelector("button[type=submit]");
  submit.disabled = true;
  els.authError.textContent = "";
  try {
    const response = await fetch(endpoint, { method: "POST", headers: syncHeaders(), body: JSON.stringify(body) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Could not sign in.");
    state.authUser = data.user;
    state.csrfToken = data.csrf_token || null;
    closeAuth();
    updateAccountUI();
    await syncProgress();
    await loadAccount();
  } catch (error) {
    els.authError.textContent = error.message;
  } finally {
    submit.disabled = false;
  }
}

async function toggleAccount() {
  if (!state.authUser) {
    openAuth();
    return;
  }
  if (!confirm("Sign out of TalkMate? Your local progress will stay on this device.")) return;
  await fetch("/api/auth/logout", { method: "POST", headers: syncHeaders() });
  state.authUser = null;
  state.csrfToken = null;
  state.sessions = [];
  renderSessionHistory();
  updateAccountUI();
}

function renderScenarios() {
  const level = getActiveLevel();
  if (!level) return;
  els.lessonCount.textContent = `${level.count} scenes, 5-8 min each`;
  els.scenarios.replaceChildren();
  (level.scenarios || []).forEach((scenario, index) => {
    const card = document.createElement("button");
    card.className = "scenario-card";
    card.innerHTML = `<span class="card-top"><span class="card-icon icon-${scenario.icon}">${iconText(scenario.icon)}</span><time>${scenario.duration}</time></span><h3>${scenario.title}</h3><p>${scenario.description}</p><span class="start-row">Start scene -></span>`;
    card.addEventListener("click", async () => {
      card.disabled = true;
      try { await startScenario(index); } catch (error) { alert("Không thể bắt đầu tình huống. Hãy kiểm tra máy chủ rồi thử lại."); } finally { card.disabled = false; }
    });
    els.scenarios.append(card);
  });
}

function addMessage(role, text) {
  const template = $("#message-template");
  const item = template.content.firstElementChild.cloneNode(true);
  item.classList.add(role);
  item.querySelector(".message-label").textContent = role === "user" ? "YOU" : "YOUR PARTNER";
  item.querySelector("p").textContent = text;
  els.chat.append(item);
  els.chat.scrollTop = els.chat.scrollHeight;
  return item;
}

function renderPractice(opening) {
  els.title.textContent = state.scenario.title;
  els.context.textContent = state.scenario.context;
  els.goal.textContent = state.level.goal;
  els.category.textContent = state.level.name.toUpperCase();
  els.icon.textContent = iconText(state.scenario.icon);
  els.icon.className = `scene-icon icon-${state.scenario.icon}`;
  els.vocabulary.replaceChildren();
  state.scenario.vocabulary.forEach((word) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = word;
    chip.title = "Click to use this phrase";
    chip.addEventListener("click", () => {
      els.input.value = `${els.input.value}${els.input.value ? " " : ""}${word}`;
      els.input.focus();
    });
    els.vocabulary.append(chip);
  });
  renderSentenceBuilder(state.scenario.sentence_builder);
  els.chat.replaceChildren();
  els.coachBox.classList.add("hidden");
  els.pronunciationBox.classList.add("hidden");
  els.finished.classList.add("hidden");
  els.composer.classList.remove("hidden");
  els.input.value = "";
  els.input.placeholder = `Try: ${state.scenario.starter}`;
  els.sessionLanguage.classList.toggle("hidden", !state.englishOnly);
  renderConversationFlow();
  updateTurnCounter();
  addMessage("partner", opening);
}

function renderConversationFlow(conversation = null) {
  if (!els.conversationGoals) return;
  const goals = conversation?.goals || state.scenario?.conversation_goals || [];
  const completed = conversation?.completed || 0;
  const total = conversation?.total || goals.length || 4;
  const taskScore = conversation?.task_score ?? 0;
  els.taskScore.textContent = `${taskScore} / 10`;
  els.taskProgress.textContent = `${completed} / ${total} moves complete`;
  els.conversationGoals.replaceChildren();
  goals.forEach((goal, index) => {
    const item = document.createElement("li");
    item.className = index < completed ? "complete" : "";
    item.textContent = goal.label;
    els.conversationGoals.append(item);
  });
}

function renderSentenceBuilder(builder) {
  els.sentenceBuilder.classList.toggle("hidden", !builder);
  if (!builder) return;
  els.builderLabel.textContent = builder.label || "BUILD A USEFUL SENTENCE";
  els.builderHint.textContent = builder.hint || "Use the frame, then make it your own.";
  els.builderFrame.textContent = builder.frame || "";
  els.builderSlots.replaceChildren();
  (builder.slots || []).forEach((slot) => {
    const label = document.createElement("label");
    label.className = "builder-slot";
    label.textContent = slot.label || "detail";
    const input = document.createElement("input");
    input.dataset.slot = slot.key;
    input.placeholder = slot.placeholder || "your words";
    input.addEventListener("input", updateBuilderPreview);
    label.append(input);
    els.builderSlots.append(label);
  });
  els.builderExamples.replaceChildren();
  (builder.examples || []).slice(0, 2).forEach((example) => {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "builder-example";
    item.textContent = example;
    item.addEventListener("click", () => {
      els.input.value = example;
      els.input.focus();
    });
    els.builderExamples.append(item);
  });
  updateBuilderPreview();
}

function buildSentence() {
  const builder = state.scenario?.sentence_builder;
  if (!builder) return "";
  const values = {};
  els.builderSlots.querySelectorAll("input").forEach((input) => { values[input.dataset.slot] = input.value.trim(); });
  return (builder.frame || "").replace(/\[([^\]]+)\]/g, (match, key) => values[key] || match);
}

function updateBuilderPreview() {
  const sentence = buildSentence();
  els.builderPreview.textContent = sentence ? `Your sentence: ${sentence}` : "Add your details to build a sentence.";
}

function updateTurnCounter() {
  const turns = state.history.filter((turn) => turn.role === "user").length;
  els.turnCounter.textContent = `${turns} / 4 turns`;
}

function renderCoaching(data) {
  els.coachBox.classList.remove("hidden");
  if (data.conversation) renderConversationFlow(data.conversation);
  els.feedback.textContent = data.feedback;
  const reason = data.scored === false ? guardReasonLabels[data.guard_reason] || "NO SCORE - try one clear sentence" : "";
  els.guardReason.textContent = reason;
  els.guardReason.classList.toggle("hidden", !reason);
  els.grammarNote.textContent = data.grammar_note || "No grammar issue to fix in this sentence.";
  els.wordChoiceNote.textContent = data.word_choice_note || "Your word choice works for this situation.";
  els.sentencePattern.textContent = data.sentence_pattern || data.improved || state.scenario?.starter || "";
  els.tip.textContent = data.tip;
  els.score.textContent = data.scored === false ? "NO SCORE" : `${data.overall}/10`;
  els.improved.textContent = data.improved;
  els.improvedWrap.classList.toggle("hidden", !data.improved);
  els.scores.replaceChildren();
  Object.entries(data.scores).forEach(([name, score]) => {
    const item = document.createElement("span");
    item.className = "score";
    item.title = scoreHints[name] || "Score for this part of your reply.";
    const label = document.createTextNode(scoreLabels[name] || name.replace("_", " "));
    const value = document.createElement("strong");
    value.textContent = score;
    item.append(label, " ", value);
    els.scores.append(item);
  });
  els.mode.textContent = data.mode === "ai" ? "AI coach" : "Guided practice";
}

function renderPronunciation(data) {
  if (!data) return;
  els.pronunciationBox.classList.remove("hidden");
  els.pronunciationLabel.textContent = data.label;
  els.pronunciationScore.textContent = `${data.score}%`;
  els.pronunciationHeard.textContent = data.heard || "-";
  els.pronunciationTip.textContent = data.tip;
  els.unclearWords.replaceChildren();
  if (!data.unclear_words?.length) {
    const clear = document.createElement("span");
    clear.className = "word-coach";
    clear.innerHTML = "<strong>All key words sound clear</strong>";
    els.unclearWords.append(clear);
    return;
  }
  data.unclear_words.forEach(({ word, tip }) => {
    const item = document.createElement("span");
    item.className = "word-coach";
    item.innerHTML = `<strong>${word}</strong><span>${tip}</span>`;
    els.unclearWords.append(item);
  });
}

function recordSession(data) {
  const progress = getProgress();
  const sceneId = `${state.level.id}-${state.scenarioIndex}`;
  if (!progress.completed.includes(sceneId)) progress.completed.push(sceneId);
  progress.scoreEvents ||= [];
  progress.scoreEvents.push({ id: eventId("score"), score: data.overall, at: new Date().toISOString() });
  progress.scoreEvents = progress.scoreEvents.slice(-30);
  progress.scores = progress.scoreEvents.map((event) => event.score);
  const today = dayStamp();
  if (!progress.activeDays.includes(today)) progress.activeDays.push(today);
  const momentum = ensureMomentum(progress);
  momentum.dailyMinutes[today] = Math.min(5, (momentum.dailyMinutes[today] || 0) + 5);
  momentum.xpEvents.push({ id: eventId("xp"), amount: 35, at: new Date().toISOString() });
  momentum.xp += 35;
  evaluateBadges(progress);
  saveProgress(progress);
  updateProgressUI();
  saveCompletedSession(data);
}

async function saveCompletedSession(data) {
  if (!state.authUser || !state.scenario) return;
  try {
    await fetch("/api/sessions", {
      method: "POST",
      headers: syncHeaders(),
      body: JSON.stringify({
        title: state.scenario.title,
        client_id: state.sessionId,
        session: {
          level: getLearnerProfile().proficiency,
          overall: data.overall,
          turns: state.history.filter((turn) => turn.role === "user").length,
          completed_at: new Date().toISOString(),
          transcript: state.history,
        },
      }),
    });
    const responseData = await response.json();
    if (!response.ok) throw new Error(responseData.error || "Could not save session");
    const sync = await fetch("/api/sync");
    if (sync.ok) {
      const data = await sync.json();
      state.sessions = Array.isArray(data.sessions) ? data.sessions : [];
      renderSessionHistory();
    }
  } catch {
    // Progress sync still preserves the key learning data if session history fails.
  }
}

function renderChallengePrompt() {
  els.challengePrompt.textContent = challengePrompts[state.challengePromptIndex % challengePrompts.length];
  els.challengeTimer.textContent = state.challengeSeconds;
}

function startChallenge() {
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    alert("Trình duyệt này chưa hỗ trợ nhận diện giọng nói cho thử thách 60 giây.");
    return;
  }
  if (state.challengeRunning) return;
  state.challengeSeconds = 60;
  state.challengeTranscript = "";
  state.challengeRunning = true;
  els.challengeTranscript.textContent = "Listening... keep going.";
  els.challengeResult.classList.add("hidden");
  els.challengeStart.classList.add("hidden");
  els.challengeStop.classList.remove("hidden");
  renderChallengePrompt();

  const recognition = new Recognition();
  recognition.lang = "en-US";
  recognition.continuous = true;
  recognition.interimResults = true;
  state.challengeRecognition = recognition;
  recognition.onresult = (event) => {
    const heard = Array.from(event.results).map((result) => result[0].transcript).join(" ").trim();
    state.challengeTranscript = heard;
    els.challengeTranscript.textContent = heard || "Listening... keep going.";
  };
  recognition.onerror = () => {
    els.challengeTranscript.textContent = "I could not hear you clearly. You can try the challenge again.";
  };
  recognition.start();
  state.challengeInterval = window.setInterval(() => {
    state.challengeSeconds -= 1;
    els.challengeTimer.textContent = state.challengeSeconds;
    if (state.challengeSeconds <= 0) finishChallenge(true);
  }, 1000);
}

function finishChallenge(fullMinute) {
  if (!state.challengeRunning) return;
  state.challengeRunning = false;
  window.clearInterval(state.challengeInterval);
  state.challengeInterval = null;
  if (state.challengeRecognition) {
    state.challengeRecognition.onresult = null;
    state.challengeRecognition.stop();
    state.challengeRecognition = null;
  }
  els.challengeStart.classList.remove("hidden");
  els.challengeStop.classList.add("hidden");
  const words = state.challengeTranscript.match(/[A-Za-z']+/g) || [];
  const hasVietnamese = /[à-ỹđ]/i.test(state.challengeTranscript);
  const speakingEnough = words.length >= 30;
  if (fullMinute) {
    const progress = getProgress();
    const momentum = ensureMomentum(progress);
    momentum.challengeEvents.push({ id: eventId("challenge"), amount: 1, at: new Date().toISOString() });
    momentum.challenges += 1;
    const xp = speakingEnough ? 55 : 35;
    momentum.xpEvents.push({ id: eventId("xp"), amount: xp, at: new Date().toISOString() });
    momentum.xp += xp;
    const today = dayStamp();
    momentum.dailyMinutes[today] = Math.min(5, (momentum.dailyMinutes[today] || 0) + 1);
    if (!progress.activeDays.includes(today)) progress.activeDays.push(today);
    evaluateBadges(progress);
    saveProgress(progress);
    updateProgressUI();
  }
  els.challengeResult.classList.remove("hidden");
  if (fullMinute && speakingEnough) {
    els.challengeResultTitle.textContent = "Brave minute complete.";
    els.challengeResultCopy.textContent = hasVietnamese
      ? `You said ${words.length} words. Try the next round with English-only thoughts.`
      : `You said ${words.length} words and earned 55 XP. That is real speaking practice.`;
  } else if (fullMinute) {
    els.challengeResultTitle.textContent = "You stayed in the moment.";
    els.challengeResultCopy.textContent = `You reached 60 seconds and earned 35 XP. Next time, aim for 30 spoken words.`;
  } else {
    els.challengeResultTitle.textContent = "A brave start.";
    els.challengeResultCopy.textContent = "No XP yet - take a breath and try a full 60-second round when you are ready.";
  }
}

function renderReviewLab() {
  const progress = getProgress();
  const allItems = progress.reviewItems || [];
  let migrated = false;
  allItems.forEach((item, index) => {
    if (!item.id) { item.id = `legacy-review-${index}`; migrated = true; }
    if (!item.category) { item.category = reviewCategoryFor(item.source, { note: item.note, tag: item.tag }); migrated = true; }
    if (!item.exercise) { item.exercise = reviewExercisePrompts[item.category] || reviewExercisePrompts.word_choice; migrated = true; }
    if (item.attempts == null) { item.attempts = 0; migrated = true; }
    if (item.correct == null) { item.correct = 0; migrated = true; }
    if (!item.lastReviewedDay) { item.lastReviewedDay = ""; migrated = true; }
  });
  if (migrated) saveProgress(progress);
  const items = state.reviewFilter === "all"
    ? allItems
    : allItems.filter((item) => (item.category || "word_choice") === state.reviewFilter);
  const stats = ensureReviewStats(progress);
  const today = dayStamp();
  const completedToday = Math.min(5, Number(stats.dailyCompleted[today]) || 0);
  els.reviewCount.textContent = `${items.length} saved correction${items.length === 1 ? "" : "s"}`;
  renderReviewProgress(progress, allItems, completedToday);
  els.reviewEmpty.classList.toggle("hidden", items.length > 0);
  els.reviewCard.classList.toggle("hidden", items.length === 0);
  if (!items.length) return;
  const pending = items.filter((item) => item.lastReviewedDay !== today);
  const pool = pending.length ? pending : items;
  const item = pool[state.reviewIndex % pool.length];
  state.reviewCurrentId = item.id || item.source;
  const category = item.category || "word_choice";
  els.reviewTag.textContent = reviewCategoryMeta[category]?.label || item.tag || "PERSONAL FIX";
  els.reviewMode.textContent = `${item.level || "A2"} · ${item.target || "practice"}`;
  els.reviewInstruction.textContent = item.exercise || reviewExercisePrompts[category] || "Rewrite this sentence in natural English.";
  els.reviewSource.textContent = item.source;
  els.reviewInput.value = "";
  els.reviewAnswer.classList.add("hidden");
  els.reviewCorrection.textContent = item.correction;
  els.reviewNote.textContent = item.note || "Compare the structure, then say the model answer out loud.";
}

function renderReviewProgress(progress, items, completedToday = 0) {
  if (els.reviewDailyProgress) {
    els.reviewDailyProgress.textContent = completedToday >= 5
      ? "Today's 5-minute review is complete"
      : `${completedToday} / 5 quick drills completed today`;
  }
  if (els.reviewDailyBar) els.reviewDailyBar.style.width = `${completedToday * 20}%`;
  if (!els.reviewCategories) return;
  const counts = items.reduce((result, item) => {
    const category = item.category || "word_choice";
    result[category] = (result[category] || 0) + 1;
    return result;
  }, {});
  els.reviewCategories.replaceChildren();
  Object.entries(reviewCategoryMeta).forEach(([category, meta]) => {
    const card = document.createElement("button");
    card.type = "button";
    card.className = `review-category${state.reviewFilter === category ? " selected" : ""}`;
    card.innerHTML = `<strong>${counts[category] || 0}</strong><span>${meta.name}</span><small>${meta.hint}</small>`;
    card.addEventListener("click", () => {
      state.reviewFilter = state.reviewFilter === category ? "all" : category;
      renderReviewLab();
    });
    els.reviewCategories.append(card);
  });
}

function reviewCategoryFor(message, data = {}) {
  const source = `${message || ""}`.toLowerCase();
  const text = `${data.grammar_note || ""} ${data.word_choice_note || ""} ${data.feedback || ""} ${data.note || ""} ${data.tag || ""}`.toLowerCase();
  const articleMistake = /\ba\s+(?:hour|honest|honor|heir|herb|[aeiou][a-z]+)\b|\ban\s+(?:university|user|usual|european|one|once|[bcdfghjklmnpqrstvwxyz][a-z]+)\b/.test(source);
  const missingArticle = /\b(?:need|want|have)\s+(?:reservation|ticket|room|table|meeting|appointment|interview|hotel|station|doctor|symptom|question|recommendation|project|plan|solution|problem|job|apartment|deposit|lease|dish)\b/.test(source);
  if (/article|mạo từ|vowel sound|singular countable/.test(text) || articleMistake || missingArticle) return "articles";
  if (/preposition|giới từ|interested in|good at|arrive at|depend on|listen to/.test(text)) return "prepositions";
  if (/word order|trật tự|helping verb|auxiliary|modal|verb form|have'|has'|didn't|chia động từ/.test(text)) {
    return /question|word order|trật tự/.test(text) ? "word_order" : "verb_forms";
  }
  return /word choice|polite|natural|cách dùng từ|từ bạn/.test(text) ? "word_choice" : "verb_forms";
}

function saveReviewItem(message, data) {
  const correction = (data.improved || "").trim();
  if (!correction || correction.toLowerCase() === message.trim().toLowerCase()) return;
  const progress = getProgress();
  progress.reviewItems ||= [];
  const duplicate = progress.reviewItems.some((item) => item.source.toLowerCase() === message.trim().toLowerCase());
  if (!duplicate) {
    const profile = getLearnerProfile();
    const category = reviewCategoryFor(message, data);
    progress.reviewItems.unshift({
      id: eventId("review"),
      source: message.trim(),
      correction,
      note: data.grammar_note || data.word_choice_note || data.feedback,
      tag: reviewCategoryMeta[category]?.label || reviewTag(data),
      category,
      exercise: reviewExercisePrompts[category],
      level: profile.proficiency,
      target: profile.target,
      attempts: 0,
      correct: 0,
      lastReviewedDay: "",
      createdAt: new Date().toISOString(),
    });
    progress.reviewItems = progress.reviewItems.slice(0, 20);
    saveProgress(progress);
  }
  renderReviewLab();
}

function reviewTag(data) {
  const notes = `${data.grammar_note || ""} ${data.word_choice_note || ""} ${data.feedback || ""}`.toLowerCase();
  if (/polite|direct|lịch sự/.test(notes)) return "POLITE ENGLISH";
  if (/word|natural|từ|cụm/.test(notes)) return "WORD CHOICE";
  return "GRAMMAR & SENTENCE";
}

function checkReviewAnswer() {
  const progress = getProgress();
  const allItems = progress.reviewItems || [];
  const items = state.reviewFilter === "all"
    ? allItems
    : allItems.filter((item) => (item.category || "word_choice") === state.reviewFilter);
  if (!items.length) return;
  const today = dayStamp();
  const pending = items.filter((item) => item.lastReviewedDay !== today);
  const pool = pending.length ? pending : items;
  const item = items.find((candidate) => (candidate.id || candidate.source) === state.reviewCurrentId)
    || pool[state.reviewIndex % pool.length];
  const normalize = (value) => value.toLowerCase().replace(/[^a-z0-9 ]/g, "").replace(/\s+/g, " ").trim();
  const matches = normalize(els.reviewInput.value) === normalize(item.correction);
  const stats = ensureReviewStats(progress);
  item.attempts = (Number(item.attempts) || 0) + 1;
  if (matches) item.correct = (Number(item.correct) || 0) + 1;
  stats.attempts += 1;
  if (matches) stats.correct += 1;
  if (item.lastReviewedDay !== today) {
    item.lastReviewedDay = today;
    stats.dailyCompleted[today] = Math.min(5, (Number(stats.dailyCompleted[today]) || 0) + 1);
    stats.sessions += 1;
  }
  saveProgress(progress);
  renderReviewProgress(progress, items, Math.min(5, Number(stats.dailyCompleted[today]) || 0));
  els.reviewAnswer.classList.remove("hidden");
  els.reviewNote.textContent = matches
    ? "Great - your rewrite matches the natural model."
    : "Compare the small details, then try the sentence once more out loud.";
}

async function sendMessage() {
  const message = els.input.value.trim();
  if (!message || state.completed) return;
  state.history.push({ role: "user", text: message });
  addMessage("user", message);
  els.input.value = "";
  els.send.disabled = true;
  const typing = addMessage("partner", "Thinking...");
  typing.classList.add("typing");
  try {
    const response = await fetch("/api/reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        level: state.level.id,
        scenario_index: state.scenarioIndex,
        difficulty: difficultyForLevel(getLearnerProfile().proficiency),
        history: state.history.slice(0, -1),
        message,
        learner: learnerForCoach(),
        english_only: state.englishOnly,
      }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Conversation unavailable");
    typing.remove();

    if (data.off_topic || data.scored === false) {
      // Keep the visible attempt for context, but do not let it advance the
      // role-play turn count or enter learning history/progress.
      const lastTurn = state.history[state.history.length - 1];
      if (lastTurn?.role === "user" && lastTurn.text === message) state.history.pop();
      state.lastPartnerReply = data.reply;
      addMessage("partner", data.reply);
      renderCoaching(data);
      speak(data.reply);
      updateTurnCounter();
      return;
    }

    state.history.push({ role: "partner", text: data.reply });
    state.lastPartnerReply = data.reply;
    addMessage("partner", data.reply);
    renderCoaching(data);
    state.pronunciationSample = data.improved || message;
    saveReviewItem(message, data);
    updateLearningMemory(message, data);
    updateTurnCounter();
    speak(data.reply);
    if (data.done) {
      state.completed = true;
      els.finished.classList.remove("hidden");
      els.composer.classList.add("hidden");
      recordSession(data);
    }
  } catch (error) {
    typing.remove();
    addMessage("partner", "I am having a little trouble right now. Please try your reply again.");
  } finally {
    els.send.disabled = false;
    els.input.focus();
  }
}

async function checkPronunciation(transcript, confidence) {
  try {
    const response = await fetch("/api/pronunciation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript, confidence }),
    });
    if (response.ok) renderPronunciation(await response.json());
  } catch {
    // Speech recognition remains useful even if the optional clarity check fails.
  }
}

function speak(text) {
  speakAtRate(text, 0.92);
}

function speakAtRate(text, rate) {
  if (!("speechSynthesis" in window) || !text) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = rate;
  const englishVoice = window.speechSynthesis.getVoices().find((voice) => voice.lang.startsWith("en"));
  if (englishVoice) utterance.voice = englishVoice;
  window.speechSynthesis.speak(utterance);
}

function toggleListening() {
  const mic = $("#btn-mic");
  const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!Recognition) {
    alert("Trình duyệt này chưa hỗ trợ nhận diện giọng nói. Bạn vẫn có thể gõ câu trả lời.");
    return;
  }
  if (state.recognition) {
    state.recognition.stop();
    return;
  }
  const recognition = new Recognition();
  recognition.lang = "en-US";
  recognition.interimResults = true;
  recognition.continuous = false;
  state.recognition = recognition;
  state.latestSpeech = null;
  mic.classList.add("recording");
  mic.innerHTML = '<span aria-hidden="true">stop</span> Listening';
  recognition.onresult = (event) => {
    const finalResults = Array.from(event.results).filter((result) => result.isFinal);
    const results = finalResults.length ? finalResults : Array.from(event.results);
    els.input.value = results.map((result) => result[0].transcript).join("");
    const confidence = results.length ? results[results.length - 1][0].confidence : null;
    state.latestSpeech = { transcript: els.input.value, confidence };
  };
  recognition.onend = () => {
    state.recognition = null;
    mic.classList.remove("recording");
    mic.innerHTML = '<span aria-hidden="true">mic</span> Speak';
    if (state.latestSpeech?.transcript) {
      state.pronunciationSample = state.latestSpeech.transcript;
      checkPronunciation(state.latestSpeech.transcript, state.latestSpeech.confidence);
    }
    els.input.focus();
  };
  recognition.onerror = () => recognition.stop();
  recognition.start();
}

async function loadApp() {
  try {
    const [healthResponse, levelResponse, libraryResponse] = await Promise.all([fetch("/api/health"), fetch("/api/levels"), fetch("/api/sentence-library")]);
    const health = await healthResponse.json();
    const data = await levelResponse.json();
    const libraryData = await libraryResponse.json();
    state.levels = data.levels;
    state.sentenceLibrary = Array.isArray(libraryData.categories) ? libraryData.categories : [];
    els.badge.textContent = health.ai ? "AI coach is live" : "Guided practice mode";
    els.badge.classList.toggle("offline", !health.ai);
    renderLevels();
    renderScenarios();
    renderSentenceLibrary();
  } catch {
    els.badge.textContent = "Coach offline";
    els.badge.classList.add("offline");
  }
  updateProgressUI();
  renderProfileUI();
  await loadAccount();
}

els.composer.addEventListener("submit", (event) => { event.preventDefault(); sendMessage(); });
els.input.addEventListener("keydown", (event) => { if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) { event.preventDefault(); sendMessage(); } });
$("#btn-exit").addEventListener("click", () => showView("home"));
$("#btn-again").addEventListener("click", () => showView("home"));
$("#btn-progress").addEventListener("click", () => { updateProgressUI(); showView("progress"); });
els.account.addEventListener("click", toggleAccount);
$("#btn-close-auth").addEventListener("click", closeAuth);
$("#btn-close-history").addEventListener("click", closeSessionHistory);
els.authLoginTab.addEventListener("click", () => setAuthMode("login"));
els.authRegisterTab.addEventListener("click", () => setAuthMode("register"));
els.authForm.addEventListener("submit", submitAuth);
$("#btn-close-progress").addEventListener("click", () => showView("home"));
$("#btn-start-from-progress").addEventListener("click", () => showView("home"));
$("#btn-sound").addEventListener("click", () => speak(state.lastPartnerReply));
$("#btn-use-sentence").addEventListener("click", () => {
  const sentence = buildSentence();
  if (sentence && !sentence.includes("[")) {
    els.input.value = sentence;
    els.input.focus();
  }
});
$("#btn-slow").addEventListener("click", () => speakAtRate(state.pronunciationSample, 0.72));
$("#btn-normal").addEventListener("click", () => speakAtRate(state.pronunciationSample, 0.92));
$("#btn-mic").addEventListener("click", toggleListening);
els.levelSelect.addEventListener("change", () => updateProfile((profile) => { profile.proficiency = els.levelSelect.value; }));
els.goalSelect.addEventListener("change", () => updateProfile((profile) => {
  const target = els.goalSelect.value;
  const goals = {
    travel: "Handle travel and everyday conversations with ease.",
    interview: "Answer interview questions clearly and confidently.",
    work: "Communicate ideas naturally at work.",
    dating: "Make warm, natural connections in English.",
  };
  profile.target = target;
  profile.goal = goals[target];
}));
els.englishOnly.addEventListener("change", () => updateProfile((profile) => { profile.englishOnly = els.englishOnly.checked; }));
$("#btn-check-review").addEventListener("click", checkReviewAnswer);
$("#btn-new-review").addEventListener("click", () => { state.reviewIndex += 1; renderReviewLab(); });
$("#btn-hear-review").addEventListener("click", () => {
  const items = getProgress().reviewItems || [];
  const item = items[state.reviewIndex % items.length];
  if (item) speakAtRate(item.correction, 0.84);
});
$("#btn-challenge").addEventListener("click", () => { renderChallengePrompt(); showView("challenge"); });
$("#btn-exit-challenge").addEventListener("click", () => showView("home"));
$("#btn-new-prompt").addEventListener("click", () => { state.challengePromptIndex += 1; renderChallengePrompt(); });
els.challengeStart.addEventListener("click", startChallenge);
els.challengeStop.addEventListener("click", () => finishChallenge(false));
$("#btn-challenge-again").addEventListener("click", () => { state.challengePromptIndex += 1; renderChallengePrompt(); startChallenge(); });
$(".brand").addEventListener("click", (event) => { event.preventDefault(); showView("home"); });
window.speechSynthesis?.addEventListener?.("voiceschanged", () => {});
loadApp();
