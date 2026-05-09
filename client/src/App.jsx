import { useState } from "react";
import API from "./services/api";

function App() {

  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState("");
  const [matchScore, setMatchScore] = useState("");
  const [loading, setLoading] = useState(false);
  const [jobDescription, setJobDescription] = useState("");

  const handleUpload = async () => {

    if (!file) {
      alert("Please select a resume");
      return;
    }

    try {

      setLoading(true);

      const token = localStorage.getItem("token");

      if (!token) {
        alert("No token found. Please login first.");
        setLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append("resume", file);

      // UPLOAD TO EXPRESS
      const uploadRes = await API.post(
        "/upload/resume",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${token}`,
          },
        }
      );

      console.log("UPLOAD RESPONSE:", uploadRes.data);

      // CALL FASTAPI
      const aiRes = await fetch(
        "http://localhost:8001/analyze-resume",
        {
          method: "POST",
      
          headers: {
            "Content-Type": "application/json",
          },
      
          body: JSON.stringify({
            job_description: jobDescription,
          }),
        }
      );

      const data = await aiRes.json();

      console.log("AI RESPONSE:", data);

      setAnalysis(data.analysis);

      setMatchScore(data.match_score);

      setLoading(false);

    } catch (error) {

      console.log(
        error.response?.data || error.message
      );

      alert(
        JSON.stringify(
          error.response?.data || error.message
        )
      );

      setLoading(false);

    }
  };

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      {/* NAVBAR */}
      <nav className="flex items-center justify-between px-10 py-5 border-b border-slate-800">

        <h1 className="text-3xl font-bold text-cyan-400">
          TalentLens AI
        </h1>

      </nav>

      {/* HERO */}
      <section className="px-10 py-16">

        <h2 className="text-5xl font-bold leading-tight">
          AI-Powered HR
          <br />
          Screening Platform
        </h2>

        <p className="text-slate-400 mt-6 text-lg max-w-2xl">
          Upload resumes, analyze candidates using AI,
          match resumes with job descriptions,
          and rank candidates intelligently.
        </p>

      </section>


        {/* JOB DESCRIPTION */}

          <section className="px-10 pb-10">

          <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800">

            <h2 className="text-2xl font-bold mb-6 text-cyan-400">
              Job Description
            </h2>

            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Example: AI Engineer with NLP, RAG, Python, FastAPI and Vector Databases..."
              className="
                w-full
                h-40
                bg-slate-950
                border
                border-slate-700
                rounded-xl
                p-4
                text-white
                outline-none
                focus:border-cyan-500
                resize-none
              "
            />

          </div>

          </section>

      {/* UPLOAD SECTION */}
      <section className="px-10">

        <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800">

          <h2 className="text-2xl font-bold mb-6">
            Upload Resume
          </h2>

          <div className="mb-6">

  <label
    htmlFor="resumeUpload"
    className="
      flex
      items-center
      justify-center
      w-full
      h-40
      border-2
      border-dashed
      border-cyan-500
      rounded-2xl
      cursor-pointer
      bg-slate-950
      hover:bg-slate-900
      transition
      duration-300
    "
  >

    <div className="text-center">

      <p className="text-cyan-400 text-lg font-semibold">
        Click to Upload Resume
      </p>

      <p className="text-slate-400 text-sm mt-2">
        PDF or DOCX Supported
      </p>

      {
        file && (
          <p className="text-white mt-4 font-medium">
            Selected: {file.name}
          </p>
        )
      }

    </div>

  </label>

  <input
    id="resumeUpload"
    type="file"
    accept=".pdf,.doc,.docx"
    onChange={(e) => setFile(e.target.files[0])}
    className="hidden"
  />

</div>

          <br />

          <button
            onClick={handleUpload}
            className="bg-cyan-500 hover:bg-cyan-600 px-6 py-3 rounded-xl font-semibold"
          >
            {
              loading
                ? "Analyzing..."
                : "Analyze Resume"
            }
          </button>

        </div>

      </section>

      {/* AI RESULT */}
      {
        analysis && (

          <section className="px-10 py-10">

            <div className="bg-slate-900 p-8 rounded-2xl border border-slate-800">

            <div>

              {/* SCORE CARD */}
              <div className="mb-8">

                <h3 className="text-2xl font-bold text-cyan-400 mb-2">
                  Suitability Score
                </h3>

                <div className="bg-slate-800 rounded-xl p-5 border border-cyan-500">

                  <h1 className="text-5xl font-bold text-cyan-400">
                    {matchScore}
                  </h1>

                  <p className="text-slate-400 mt-2">
                    Calculated using AI semantic similarity,
                    skill matching, projects, and technologies.
                  </p>

                </div>

              </div>

              {/* AI ANALYSIS */}
              <pre className="whitespace-pre-wrap text-slate-300 leading-8">
                {analysis}
              </pre>

              </div>

            </div>

          </section>

        )
      }

    </div>
  );
}

export default App;