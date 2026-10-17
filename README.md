<div align="center">

  <!-- Cover Banner -->
  <img src="YOUR_COVER_IMAGE_URL_OR_PATH_HERE" alt="MicroBrand Voice Engine Banner" width="100%" />

  <br/><br/>

  <p align="center">
    <b>An autonomous marketing engine that transforms raw product specs into brand-compliant, multi-platform copy and audio voiceovers with zero voice drift.</b>
  </p>

  <p align="center">
    <a href="https://microbrand-engine.onrender.com/"><img src="https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Live Demo" /></a>
    <a href="https://github.com/Anubrata-Mallick/microbrand-engine"><img src="https://img.shields.io/badge/Source-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub Repo" /></a>
    <a href="https://dev.to/challenges/hacktoberfest-week2-2026-10-12"><img src="https://img.shields.io/badge/Hacktoberfest-Week%202-FF7B1C?style=for-the-badge&logo=hacktoberfest&logoColor=white" alt="Hacktoberfest" /></a>
  </p>

  <p align="center">
    <img src="https://img.shields.io/badge/Orchestrator-LangGraph-1C3C3C?style=flat-square" />
    <img src="https://img.shields.io/badge/Memory-Backboard.io-6366F1?style=flat-square" />
    <img src="https://img.shields.io/badge/Inference-Groq-F55036?style=flat-square" />
    <img src="https://img.shields.io/badge/Voiceover-ElevenLabs-000000?style=flat-square" />
    <img src="https://img.shields.io/badge/Observability-Sentry-362D59?style=flat-square&logo=sentry" />
    <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat-square&logo=streamlit" />
  </p>

</div>

<hr />

## ⚡ At a Glance

<table>
  <tr>
    <td width="50%">
      <h3>The Dilemma</h3>
      <p>Boutique makers and solo founders waste hours manually writing tailored copy for Shopify, Instagram, and Amazon. Standard LLM prompts forget brand personas between sessions and constantly invent generic buzzwords (<em>"bargain"</em>, <em>"crazy sale"</em>) that degrade luxury or artisan brands.</p>
    </td>
    <td width="50%">
      <h3>The Solution</h3>
      <p><b>MicroBrand Voice Engine</b> stores brand tone, signature slogans, and negative constraints in persistent assistant memory, runs a 3-stage critique state machine, generates targeted copy, and creates realistic spoken voiceovers for social reels.</p>
    </td>
  </tr>
</table>

<br/>

<div align="center">
  <img src="YOUR_STREAMLIT_APP_IMAGE_URL_OR_PATH_HERE" alt="MicroBrand Web Application Interface" width="100%" />
  <p><i>Live Streamlit UI: Persistent Brand Workspace &bull; Multi-Channel Copy &bull; Spoken Voiceover Playback</i></p>
</div>

<hr />


<hr />


## 🏆 Hackathon & Sponsor Shoutouts
<details>
  <summary><b>Click to open/close</b></summary>
  
This project was built for the **Hacktoberfest 2026 Open-Source AI Challenge (Week 2: Side Hustle)**. Huge shoutout to the event partners whose developer platforms made building and running this engine seamless:

<table>
  <tr>
    <td width="25%" align="center">
      <a href="https://render.com/">
        <img src="https://img.shields.io/badge/Render-Hosted%20Cloud-46E3B7?style=for-the-badge&logo=render&logoColor=white" /><br/>
        <b>Render</b>
      </a>
      <p>Declarative continuous deployment via <code>render.yaml</code> with environment variable management and automated web hosting.</p>
    </td>
    <td width="25%" align="center">
      <a href="https://sentry.io/">
        <img src="https://img.shields.io/badge/Sentry-Agent%20Tracing-362D59?style=for-the-badge&logo=sentry&logoColor=white" /><br/>
        <b>Sentry</b>
      </a>
      <p>Granular LLM agent observability, tracking token consumption, agent run roots, and debugging async event loop errors.</p>
    </td>
    <td width="25%" align="center">
      <a href="https://backboard.io/">
        <img src="https://img.shields.io/badge/Backboard-Assistant%20Memory-6366F1?style=for-the-badge&logo=probot&logoColor=white" /><br/>
        <b>Backboard.io</b>
      </a>
      <p>Persistent assistant memory keeping brand guidelines, forbidden buzzwords, and tone identity intact across sessions.</p>
    </td>
    <td width="25%" align="center">
      <a href="https://elevenlabs.io/">
        <img src="https://img.shields.io/badge/ElevenLabs-Voice%20Synthesis-000000?style=for-the-badge&logo=elevenlabs&logoColor=white" /><br/>
        <b>ElevenLabs</b>
      </a>
      <p>Instant audio voiceover synthesis for testing and previewing social scripts inside the Streamlit workspace.</p>
    </td>
  </tr>
</table>

<br/>

<div align="center">
  <p>
    📖 <b>Read the complete write-up and technical deep dive:</b><br/>
    <a href="YOUR_DEV_TO_POST_URL_HERE"><b>👉 Read on DEV.to: MicroBrand Voice Engine: An Agentic Copywriter</b></a>
  </p>
</div>
</details>
  
## 🧠 Core Architecture
<details open>
  <summary><b>1. Persistent Memory (Backboard.io)</b></summary>
  <blockquote>
    Eliminates repetitive system prompting. Brand identity, tone constraints (e.g., <i>"Minimalist, adventurous, quiet confidence"</i>), and forbidden phrasing persist across sessions inside an active assistant workspace.
  </blockquote>
</details>

<details>
  <summary><b>2. Multi-Channel Generation (Groq High-Speed Inference)</b></summary>
  <blockquote>
    Generates structured, platform-native outputs simultaneously:
    <ul>
      <li><b>Shopify:</b> Storytelling prose emphasizing craft and material feel.</li>
      <li><b>Instagram:</b> Punchy social hooks with hashtag targeting and spoken audio scripts.</li>
      <li><b>Amazon:</b> Conversion-optimized bullet points focused on specs and features.</li>
    </ul>
  </blockquote>
</details>

<details>
  <summary><b>3. Automated Compliance Guardrail (LangGraph Node)</b></summary>
  <blockquote>
    Every draft passes through an automated critique node that cross-references text against forbidden negative constraints. Buzzwords are detected and scrubbed prior to UI delivery.
  </blockquote>
</details>

<details>
  <summary><b>4. Audio Narration (ElevenLabs)</b></summary>
  <blockquote>
    Transforms written social scripts into natural, broadcast-ready voiceovers so creators can immediately audition audio hooks for TikTok, Reels, and Shorts.
  </blockquote>
</details>

<hr />

## 📡 Observability & Agent Tracing (Sentry)

To ensure sub-second reliability, prevent silent LLM drift, and monitor token economics in production, **Sentry Agent Tracing** (`sentry-sdk`) is integrated across all LangGraph nodes and API spans.

<br/>

<div align="center">
  <img src="YOUR_SENTRY_IMAGE_URL_OR_PATH_HERE" alt="Sentry Agents Telemetry Dashboard" width="100%" />
  <p><i>Real telemetry in Sentry: LangGraph root traces, per-run token accounting, and cost tracking.</i></p>
</div>

<table>
  <tr>
    <th align="left">Metric</th>
    <th align="left">Observed Telemetry in Sentry</th>
  </tr>
  <tr>
    <td><b>Agent Root Tracing</b></td>
    <td>Automatically grouped under <code>LangGraph</code> with precise runtime tracking across turns (3.39s – 6.80s).</td>
  </tr>
  <tr>
    <td><b>Token & Cost Accounting</b></td>
    <td>Exact per-run token tracking (649, 745, 821, 827 tokens) with automated cost estimation graphs.</td>
  </tr>
  <tr>
    <td><b>Error Diagnostics</b></td>
    <td>Traced and resolved an asynchronous <code>httpx</code> event-loop error (<code>ea0fae1f</code>) by offloading calls to dedicated runners.</td>
  </tr>
</table>

<hr />

## 🚀 Quickstart & Local Setup

<details>
  <summary><b>1. Clone the repository</b></summary>

```bash
git clone [https://github.com/Anubrata-Mallick/microbrand-engine.git](https://github.com/Anubrata-Mallick/microbrand-engine.git)
cd microbrand-engine
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
</details>
<details>
<summary><b>2. Create the .env file</b></summary>

```bash
BACKBOARD_API_KEY=your_backboard_api_key
GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
SENTRY_DSN=your_sentry_dsn
```
</details>
<details>
<summary><b>3. Run the app </b></summary>

```bash
streamlit run app.py
```
</details>
