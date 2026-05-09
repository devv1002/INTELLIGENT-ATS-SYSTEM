import jsPDF from "jspdf";
import { useState } from "react";
import API from "./services/api";

function App() {

  const [files, setFiles] = useState([]);

  const [rankedCandidates, setRankedCandidates] = useState([]);

  const [candidateStatus, setCandidateStatus] = useState({});

  const [loading, setLoading] = useState(false);

  const [jobDescription, setJobDescription] = useState("");


  // UPDATE STATUS
  const updateCandidateStatus = (
    index,
    status
  ) => {

    setCandidateStatus((prev) => ({

      ...prev,

      [index]: status,

    }));
  };


  // PDF REPORT DOWNLOAD
  const downloadPDFReport = () => {

    const doc = new jsPDF();

    let y = 20;

    doc.setFontSize(22);

    doc.text(
      "TalentLens AI - Candidate Ranking Report",
      20,
      y
    );

    y += 20;

    rankedCandidates.forEach((candidate, index) => {

      doc.setFontSize(18);

      doc.text(
        `Rank #${index + 1}`,
        20,
        y
      );

      y += 10;

      doc.setFontSize(12);

      doc.text(
        `Resume: ${candidate.resume_path}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Final Weighted Score: ${candidate.final_score}/10`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Semantic Score: ${candidate.semantic_score}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Skill Score: ${candidate.skill_score}/10`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Project Score: ${candidate.project_score}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Experience Score: ${candidate.experience_score}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Matched Skills: ${candidate.matched_skills.join(", ")}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Missing Skills: ${candidate.missing_skills.join(", ")}`,
        20,
        y
      );

      y += 10;

      doc.text(
        `Status: ${
          candidateStatus[index] || "PENDING"
        }`,
        20,
        y
      );

      y += 20;

      // NEW PAGE
      if (y > 250) {

        doc.addPage();

        y = 20;
      }

    });

    doc.save("TalentLens_Report.pdf");
  };


  // HANDLE UPLOAD
  const handleUpload = async () => {

    if (files.length === 0) {

      alert("Please select resumes");

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

      files.forEach((file) => {

        formData.append("resumes", file);

      });

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

      console.log(
        "UPLOAD RESPONSE:",
        uploadRes.data
      );

      // EXTRACT FILE PATHS
      const uploadedFiles =
        uploadRes.data.files;

      const resumePaths =
        uploadedFiles.map(
          (file) => file.path
        );

      console.log(
        "RESUME PATHS:",
        resumePaths
      );

      // CALL FASTAPI
      const aiRes = await fetch(

        "http://localhost:8001/analyze-resume",

        {
          method: "POST",

          headers: {

            "Content-Type": "application/json",
          
            "x-api-key": "talentlens_secure_api"
          },

          body: JSON.stringify({

            job_description: jobDescription,

            resume_paths: resumePaths,

          }),
        }
      );

      const data = await aiRes.json();

      console.log(
        "AI RESPONSE:",
        data
      );

      setRankedCandidates(
        data.ranked_candidates
      );

      setLoading(false);

    } catch (error) {

      console.log(
        error.response?.data ||
        error.message
      );

      alert(

        JSON.stringify(

          error.response?.data ||
          error.message
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

            onChange={(e) =>
              setJobDescription(e.target.value)
            }

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

            Upload Resumes

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

                  Click to Upload Resumes

                </p>

                <p className="text-slate-400 text-sm mt-2">

                  PDF or DOCX Supported

                </p>

                {
                  files.length > 0 && (

                    <div className="mt-4">

                      {
                        files.map((file, index) => (

                          <p
                            key={index}
                            className="text-white font-medium"
                          >
                            {file.name}
                          </p>

                        ))
                      }

                    </div>
                  )
                }

              </div>

            </label>

            <input
              id="resumeUpload"

              type="file"

              multiple

              accept=".pdf,.doc,.docx"

              onChange={(e) =>
                setFiles([...e.target.files])
              }

              className="hidden"
            />

          </div>

          <button

            onClick={handleUpload}

            className="
              bg-cyan-500
              hover:bg-cyan-600
              px-6
              py-3
              rounded-xl
              font-semibold
            "
          >

            {
              loading
                ? "Analyzing..."
                : "Analyze Resumes"
            }

          </button>

        </div>

      </section>


      {/* RANKED CANDIDATES */}
      {
        rankedCandidates.length > 0 && (

          <section className="px-10 py-10">

            <div className="flex items-center justify-between mb-8">

              <h2 className="text-4xl font-bold text-cyan-400">

                Ranked Candidates

              </h2>

              <button

                onClick={downloadPDFReport}

                className="
                  bg-cyan-500
                  hover:bg-cyan-600
                  px-6
                  py-3
                  rounded-xl
                  font-semibold
                "
              >

                Download PDF Report

              </button>

            </div>

            <div className="space-y-8">

              {
                rankedCandidates.map((candidate, index) => (

                  <div

                    key={index}

                    className="
                      bg-slate-900
                      border
                      border-slate-800
                      rounded-2xl
                      p-8
                    "
                  >

                    {/* HEADER */}
                    <div className="flex justify-between items-center mb-8">

                      <div>

                      <div className="flex items-center gap-4">

                          <h2 className="text-3xl font-bold">

                            Rank #{index + 1}

                          </h2>

                          {/* AI RECOMMENDATION */}
                          <span
                            className={`
                              px-4
                              py-2
                              rounded-full
                              text-sm
                              font-bold

                              ${
                                candidate.recommendation === "SHORTLIST"

                                  ? "bg-green-500/20 text-green-400"

                                  : candidate.recommendation === "HOLD"

                                  ? "bg-yellow-500/20 text-yellow-400"

                                  : "bg-red-500/20 text-red-400"
                              }
                            `}
                          >

                            {candidate.recommendation}

                          </span>

                          {/* HR OVERRIDE */}
                          <span
                            className={`
                              px-4
                              py-2
                              rounded-full
                              text-sm
                              font-semibold

                              ${
                                candidateStatus[index] === "SHORTLISTED"

                                  ? "bg-green-500/20 text-green-400"

                                  : candidateStatus[index] === "REJECTED"

                                  ? "bg-red-500/20 text-red-400"

                                  : "bg-slate-700 text-slate-300"
                              }
                            `}
                          >

                            {
                              candidateStatus[index] || "HR PENDING"
                            }

                          </span>

                          </div>

                        <p className="text-slate-400 mt-2">

                          {candidate.resume_path}

                        </p>

                      </div>

                      <div className="text-right">

                        <h1 className="text-6xl font-bold text-cyan-400">

                          {candidate.final_score}

                        </h1>

                        <p className="text-slate-400">

                          Final Score

                        </p>

                      </div>

                    </div>


                    {/* SCORE CARDS */}
                    {/* SCORE CARDS */}
                      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">

                      {/* SKILLS */}
                      <div className="bg-slate-800 p-5 rounded-xl">

                        <p className="text-slate-400">
                          Skills
                        </p>

                        <h3 className="text-3xl font-bold mt-2">
                          {candidate.skills_score}
                        </h3>

                      </div>

                      {/* EXPERIENCE */}
                      <div className="bg-slate-800 p-5 rounded-xl">

                        <p className="text-slate-400">
                          Experience
                        </p>

                        <h3 className="text-3xl font-bold mt-2">
                          {candidate.experience_score}
                        </h3>

                      </div>

                      {/* EDUCATION */}
                      <div className="bg-slate-800 p-5 rounded-xl">

                        <p className="text-slate-400">
                          Education
                        </p>

                        <h3 className="text-3xl font-bold mt-2">
                          {candidate.education_score}
                        </h3>

                      </div>

                      {/* PROJECTS */}
                      <div className="bg-slate-800 p-5 rounded-xl">

                        <p className="text-slate-400">
                          Projects
                        </p>

                        <h3 className="text-3xl font-bold mt-2">
                          {candidate.project_score}
                        </h3>

                      </div>

                      {/* COMMUNICATION */}
                      <div className="bg-slate-800 p-5 rounded-xl">

                        <p className="text-slate-400">
                          Communication
                        </p>

                        <h3 className="text-3xl font-bold mt-2">
                          {candidate.communication_score}
                        </h3>

                      </div>

                      </div>


                    {/* SKILLS */}
                    <div className="grid md:grid-cols-2 gap-8 mb-8">

                      {/* MATCHED */}
                      <div className="bg-slate-800 p-6 rounded-2xl">

                        <h3 className="text-2xl font-bold text-green-400 mb-4">

                          Matched Skills

                        </h3>

                        <div className="flex flex-wrap gap-3">

                          {
                            candidate.matched_skills.map(
                              (skill, idx) => (

                                <span
                                  key={idx}

                                  className="
                                    bg-green-500/20
                                    text-green-400
                                    px-4
                                    py-2
                                    rounded-full
                                  "
                                >
                                  {skill}
                                </span>

                              )
                            )
                          }

                        </div>

                      </div>


                      {/* MISSING */}
                      <div className="bg-slate-800 p-6 rounded-2xl">

                        <h3 className="text-2xl font-bold text-red-400 mb-4">

                          Missing Skills

                        </h3>

                        <div className="flex flex-wrap gap-3">

                          {
                            candidate.missing_skills.map(
                              (skill, idx) => (

                                <span
                                  key={idx}

                                  className="
                                    bg-red-500/20
                                    text-red-400
                                    px-4
                                    py-2
                                    rounded-full
                                  "
                                >
                                  {skill}
                                </span>

                              )
                            )
                          }

                        </div>

                      </div>

                    </div>


                    {/* ACTION BUTTONS */}
                    <div className="flex gap-4 mb-8">

                      <button

                        onClick={() =>
                          updateCandidateStatus(
                            index,
                            "SHORTLISTED"
                          )
                        }

                        className="
                          bg-green-500
                          hover:bg-green-600
                          px-6
                          py-3
                          rounded-xl
                          font-semibold
                        "
                      >

                        Shortlist

                      </button>

                      <button

                        onClick={() =>
                          updateCandidateStatus(
                            index,
                            "REJECTED"
                          )
                        }

                        className="
                          bg-red-500
                          hover:bg-red-600
                          px-6
                          py-3
                          rounded-xl
                          font-semibold
                        "
                      >

                        Reject

                      </button>

                    </div>


                    {/* AI ANALYSIS */}
                    <div>

                      <h3 className="text-3xl font-bold text-cyan-400 mb-6">

                        AI Analysis

                      </h3>

                      <pre className="
                        whitespace-pre-wrap
                        text-slate-300
                        leading-8
                      ">
                        {candidate.analysis}
                      </pre>

                    </div>

                  </div>

                ))
              }

            </div>

          </section>

        )
      }

    </div>
  );
}

export default App;