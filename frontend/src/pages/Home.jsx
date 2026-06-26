import { useEffect, useRef, useState } from 'react';
import Navbar from '../components/Navbar';
import UploadForm from '../components/UploadForm';
import { createAdvice, createInterviewQuestions, generateReport } from '../../api/api';

function Home() {
  const [analysis, setAnalysis] = useState(null);
  const [advice, setAdvice] = useState(null);
  const [interview, setInterview] = useState(null);
  const [featureLoading, setFeatureLoading] = useState(false);
  const [featureError, setFeatureError] = useState('');
  const resultsRef = useRef(null);
  const adviceRef = useRef(null);
  const interviewRef = useRef(null);

  const scrollIntoView = (ref) => {
    requestAnimationFrame(() => {
      ref.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  };

  useEffect(() => {
    if (analysis) {
      scrollIntoView(resultsRef);
    }
  }, [analysis]);

  useEffect(() => {
    if (advice) {
      scrollIntoView(adviceRef);
    }
  }, [advice]);

  useEffect(() => {
    if (interview) {
      scrollIntoView(interviewRef);
    }
  }, [interview]);

  const handleGenerateAdvice = async () => {
    if (!analysis) return;
    setFeatureError('');
    setFeatureLoading(true);

    try {
      const response = await createAdvice({
        ats_score: analysis.ats_score,
        matched_skills: analysis.matched_skills,
        missing_skills: analysis.missing_skills,
        strong_evidence: analysis.skill_evidence?.strong ?? [],
        limited_evidence: analysis.skill_evidence?.limited ?? [],
        projects_text: analysis.projects_text || '',
        experience_text: analysis.experience_text || '',
      });
      setAdvice(response.data);
    } catch (error) {
      setFeatureError(error?.response?.data?.detail || error.message || 'Failed to generate advice.');
    } finally {
      setFeatureLoading(false);
    }
  };

  const handleGenerateInterview = async () => {
    if (!analysis) return;
    setFeatureError('');
    setFeatureLoading(true);

    try {
      const response = await createInterviewQuestions({ analysis });
      setInterview(response.data);
    } catch (error) {
      setFeatureError(error?.response?.data?.detail || error.message || 'Failed to generate interview questions.');
    } finally {
      setFeatureLoading(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!analysis || !advice) {
      setFeatureError('Generate career advice first before downloading the PDF report.');
      return;
    }

    setFeatureError('');
    setFeatureLoading(true);

    try {
      const response = await generateReport({ analysis, advice });
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = 'ATS_Report.pdf';
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (error) {
      setFeatureError(error?.response?.data?.detail || error.message || 'Failed to download report.');
    } finally {
      setFeatureLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />

      <main className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
        <div className="grid gap-10 xl:grid-cols-[0.9fr_1.1fr] xl:items-start xl:gap-12">
          <section className="rounded-3xl bg-gradient-to-br from-slate-900 via-slate-800 to-slate-950 px-8 py-12 text-white shadow-2xl shadow-slate-950/20 sm:px-10 sm:py-14">
            <p className="text-sm uppercase tracking-[0.28em] text-slate-300">
              Resume analysis made simple
            </p>
            <h1 className="mt-6 text-4xl font-semibold leading-tight sm:text-5xl">
              Turn your resume into a job-ready story.
            </h1>
            <p className="mt-6 max-w-xl text-slate-300 sm:text-lg">
              Upload your resume, paste a job description, and get a faster way to understand how your experience aligns with the role.
            </p>
            <div className="mt-10 space-y-4 rounded-3xl border border-white/10 bg-white/5 p-6 text-sm text-slate-200 sm:p-8">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-800 text-white">
                  1
                </div>
                <p>Upload your resume PDF.</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-800 text-white">
                  2
                </div>
                <p>Paste the job description you want to compare.</p>
              </div>
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-slate-800 text-white">
                  3
                </div>
                <p>Run the analysis to preview insights.</p>
              </div>
            </div>
          </section>

          <div className="space-y-6">
            <UploadForm onAnalysis={setAnalysis} />

            <section className="rounded-3xl border border-slate-200/80 bg-white p-6 shadow-xl shadow-slate-200/50 sm:p-8">
              <h2 className="text-lg font-semibold text-slate-900">Why this helps</h2>
              <p className="mt-4 text-slate-600">
                Use the resume analysis workflow to identify gaps, highlight relevant skills, and speed up your job application preparation.
              </p>
              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="font-semibold text-slate-900">PDF-focused upload</p>
                  <p className="mt-2 text-sm text-slate-600">Easily attach a resume in PDF format.</p>
                </div>
                <div className="rounded-3xl bg-slate-50 p-4">
                  <p className="font-semibold text-slate-900">Job description input</p>
                  <p className="mt-2 text-sm text-slate-600">Keep the role context in one place for cleaner analysis.</p>
                </div>
              </div>
            </section>
          </div>
        </div>

        {analysis && (
          <section ref={resultsRef} className="mt-10 rounded-3xl bg-white p-6 shadow-xl shadow-slate-200/40 sm:p-8">
            <div className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Analysis results</p>
                <h2 className="mt-2 text-2xl font-semibold text-slate-900">Full resume analysis</h2>
              </div>
              <div className="rounded-3xl bg-slate-50 px-4 py-3 text-sm text-slate-700 shadow-sm shadow-slate-200/80">
                File: <span className="font-semibold text-slate-900">{analysis.filename}</span>
              </div>
            </div>

            <div className="mb-6 rounded-3xl border border-slate-200 bg-slate-50 p-4 shadow-sm shadow-slate-200/60">
              <p className="text-sm text-slate-700">Review your analysis below, then use the action buttons under the bonus skills section for tailored advice, interview prep, or a downloadable report.</p>
            </div>
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">ATS score</p>
                <p className="mt-3 text-3xl font-semibold text-slate-900">{analysis.ats_score.toFixed(1)}</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">Skill match</p>
                <p className="mt-3 text-3xl font-semibold text-slate-900">{analysis.skill_match_score.toFixed(1)}</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">Similarity</p>
                <p className="mt-3 text-3xl font-semibold text-slate-900">{analysis.similarity_score.toFixed(1)}</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-5">
                <p className="text-sm text-slate-500">Matched skills</p>
                <p className="mt-3 text-3xl font-semibold text-slate-900">{analysis.matched_skills.length}</p>
              </div>
            </div>

            <div className="mt-8 grid gap-4 lg:grid-cols-3">
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Matched skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.matched_skills.length > 0 ? (
                    analysis.matched_skills.map((skill) => (
                      <span key={skill} className="rounded-full bg-slate-100 px-3 py-1">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No matched skills found.</p>
                  )}
                </div>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Missing skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.missing_skills.length > 0 ? (
                    analysis.missing_skills.map((skill) => (
                      <span key={skill} className="rounded-full bg-rose-100 px-3 py-1 text-rose-700">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>None - great coverage.</p>
                  )}
                </div>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Bonus skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.bonus_skills.length > 0 ? (
                    analysis.bonus_skills.map((skill) => (
                      <span key={skill} className="rounded-full bg-emerald-100 px-3 py-1 text-emerald-700">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No bonus skills identified.</p>
                  )}
                </div>
              </div>
            </div>

            <div className="mt-8 grid gap-4 lg:grid-cols-2">
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Strong evidence skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.skill_evidence?.strong?.length > 0 ? (
                    analysis.skill_evidence.strong.map((skill) => (
                      <span key={skill} className="rounded-full bg-emerald-100 px-3 py-1 text-emerald-700">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No strong evidence skills found.</p>
                  )}
                </div>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Limited evidence skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.skill_evidence?.limited?.length > 0 ? (
                    analysis.skill_evidence.limited.map((skill) => (
                      <span key={skill} className="rounded-full bg-amber-100 px-3 py-1 text-amber-700">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No limited evidence skills found.</p>
                  )}
                </div>
              </div>
            </div>

            <div className="mt-8 grid gap-4 lg:grid-cols-2">
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Extracted resume skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.resume_skills.length > 0 ? (
                    analysis.resume_skills.map((skill) => (
                      <span key={skill} className="rounded-full bg-slate-100 px-3 py-1">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No resume skills extracted.</p>
                  )}
                </div>
              </div>
              <div className="rounded-3xl bg-white p-6 shadow-sm shadow-slate-200/60">
                <p className="text-sm font-medium text-slate-700">Extracted job description skills</p>
                <div className="mt-4 flex flex-wrap gap-2 text-sm text-slate-600">
                  {analysis.job_description_skills.length > 0 ? (
                    analysis.job_description_skills.map((skill) => (
                      <span key={skill} className="rounded-full bg-slate-100 px-3 py-1">
                        {skill}
                      </span>
                    ))
                  ) : (
                    <p>No JD skills extracted.</p>
                  )}
                </div>
              </div>
            </div>

            <div className="mt-8 rounded-3xl bg-slate-50 p-6 shadow-sm shadow-slate-200/70">
              <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Action center</p>
                  <h3 className="mt-2 text-xl font-semibold text-slate-900">Generate your next step</h3>
                  <p className="mt-2 text-sm text-slate-600">Create targeted advice, prep interview questions, or download your resume report.</p>
                </div>
                <div className="flex flex-wrap gap-3">
                  <button
                    type="button"
                    onClick={handleGenerateAdvice}
                    disabled={featureLoading}
                    className="rounded-3xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                  >
                    Generate Advice
                  </button>
                  <button
                    type="button"
                    onClick={handleGenerateInterview}
                    disabled={featureLoading}
                    className="rounded-3xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
                  >
                    Generate Interview Questions
                  </button>
                  <button
                    type="button"
                    onClick={handleDownloadReport}
                    disabled={featureLoading || !advice}
                    className="rounded-3xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-400"
                  >
                    Download PDF Report
                  </button>
                </div>
              </div>
              {featureError && (
                <p className="mt-4 rounded-3xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
                  {featureError}
                </p>
              )}
              {featureLoading && (
                <p className="mt-4 text-sm text-slate-600">Processing request, please wait...</p>
              )}
            </div>

            {advice && (
              <div ref={adviceRef} className="mt-6 rounded-3xl bg-white p-4 text-sm text-slate-700 shadow-sm shadow-slate-200/60">

                <div className="mt-4 grid gap-4 lg:grid-cols-3">
                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Strengths</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {advice.strengths.length > 0 ? (
                        advice.strengths.map((item, index) => (
                          <p key={`strength-${index}`}>• {item}</p>
                        ))
                      ) : (
                        <p>No strengths available.</p>
                      )}
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Improvement areas</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {advice.improvement_areas.length > 0 ? (
                        advice.improvement_areas.map((item, index) => (
                          <p key={`improvement-${index}`}>• {item}</p>
                        ))
                      ) : (
                        <p>No improvements available.</p>
                      )}
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Learning roadmap</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {advice.learning_roadmap.length > 0 ? (
                        advice.learning_roadmap.map((item, index) => (
                          <p key={`roadmap-${index}`}>• {item}</p>
                        ))
                      ) : (
                        <p>No roadmap available.</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-4 rounded-3xl bg-slate-50 p-4">
                  <p className="text-sm font-semibold text-slate-700">Interview readiness</p>
                  <p className="mt-3 text-sm text-slate-600">
                    <span className="font-semibold text-slate-900">Level:</span> {advice.interview_readiness.level}
                  </p>
                  <p className="mt-2 text-sm text-slate-600">
                    <span className="font-semibold text-slate-900">Score:</span> {advice.interview_readiness.score}</p>
                  <p className="mt-2 text-sm text-slate-600">{advice.interview_readiness.reason}</p>
                </div>
              </div>
            )}

            {interview && (
              <div ref={interviewRef} className="mt-6 rounded-3xl bg-white p-4 text-sm text-slate-700 shadow-sm shadow-slate-200/60">

                <div className="mt-4 grid gap-4 lg:grid-cols-2">
                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Technical questions</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {interview.technical_questions.length > 0 ? (
                        interview.technical_questions.map((q, index) => (
                          <p key={`tech-${index}`}>• {q}</p>
                        ))
                      ) : (
                        <p>No technical questions generated.</p>
                      )}
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Project questions</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {interview.project_questions.length > 0 ? (
                        interview.project_questions.map((q, index) => (
                          <p key={`proj-${index}`}>• {q}</p>
                        ))
                      ) : (
                        <p>No project questions generated.</p>
                      )}
                    </div>
                  </div>
                </div>

                <div className="mt-4 grid gap-4 lg:grid-cols-2">
                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">Behavioral questions</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {interview.behavioral_questions.length > 0 ? (
                        interview.behavioral_questions.map((q, index) => (
                          <p key={`beh-${index}`}>• {q}</p>
                        ))
                      ) : (
                        <p>No behavioral questions generated.</p>
                      )}
                    </div>
                  </div>

                  <div className="rounded-3xl bg-slate-50 p-4">
                    <p className="text-sm font-semibold text-slate-700">HR questions</p>
                    <div className="mt-3 space-y-2 text-slate-600">
                      {interview.hr_questions.length > 0 ? (
                        interview.hr_questions.map((q, index) => (
                          <p key={`hr-${index}`}>• {q}</p>
                        ))
                      ) : (
                        <p>No HR questions generated.</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </section>
        )}
      </main>
    </div>
  );
}

export default Home;
