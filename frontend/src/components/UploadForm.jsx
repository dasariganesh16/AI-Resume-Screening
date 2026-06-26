import { useState } from 'react';
import { analyzeResume } from '../../api/api';

function UploadForm({ onAnalysis }) {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleResumeChange = (event) => {
    const file = event.target.files?.[0] ?? null;
    setResumeFile(file);
    setErrorMessage('');
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setErrorMessage('');

    if (!resumeFile) {
      setErrorMessage('Please upload a PDF resume before analyzing.');
      return;
    }

    if (!jobDescription.trim()) {
      setErrorMessage('Please paste a job description to compare your resume against.');
      return;
    }

    if (!resumeFile.name.toLowerCase().endsWith('.pdf')) {
      setErrorMessage('Only PDF resume files are supported.');
      return;
    }

    const formData = new FormData();
    formData.append('resume', resumeFile);
    formData.append('job_description', jobDescription.trim());

    setIsLoading(true);

    try {
      const response = await analyzeResume(formData);
      onAnalysis?.(response.data);
    } catch (error) {
      console.error('Analyze request failed', error);
      const backendDetail = error?.response?.data?.detail || error?.response?.data || null;
      const status = error?.response?.status;
      const message = backendDetail
        ? `Request failed (${status}): ${backendDetail}`
        : error.message || 'Resume analysis failed.';
      setErrorMessage(message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section id="upload" className="rounded-3xl bg-white p-6 shadow-xl shadow-slate-200/70 sm:p-8">
      <div className="mb-6">
        <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Upload resume</p>
        <h2 className="mt-3 text-2xl font-semibold text-slate-900 sm:text-3xl">
          Analyze your resume against any job description.
        </h2>
        <p className="mt-3 max-w-2xl text-slate-600">
          Select your resume PDF, paste the job description, and get ready to review insights.
        </p>
      </div>

      <form className="space-y-6" onSubmit={handleSubmit}>
        <div className="grid gap-6 sm:grid-cols-[1fr_auto] sm:items-end">
          <div className="space-y-2">
            <label htmlFor="resume" className="text-sm font-medium text-slate-700">
              Resume PDF
            </label>
            <div className="rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4">
              <div className="text-sm text-slate-600">
                {resumeFile ? resumeFile.name : 'Upload your resume in PDF format'}
              </div>
            </div>
          </div>
          <label className="inline-flex cursor-pointer items-center justify-center rounded-3xl bg-slate-900 px-6 py-4 text-sm font-medium text-white transition hover:bg-slate-800">
            Browse
            <input
              id="resume"
              type="file"
              accept="application/pdf"
              className="sr-only"
              onChange={handleResumeChange}
            />
          </label>
        </div>

        <div className="space-y-2">
          <label htmlFor="jobDescription" className="text-sm font-medium text-slate-700">
            Job Description
          </label>
          <textarea
            id="jobDescription"
            rows="8"
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            placeholder="Paste the job description here"
            className="w-full rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-900 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200"
          />
        </div>

        {errorMessage && (
          <p className="rounded-3xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
            {errorMessage}
          </p>
        )}

        <button
          type="submit"
          disabled={isLoading}
          className="inline-flex items-center justify-center rounded-3xl bg-slate-900 px-6 py-3 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isLoading ? (
            <>
              <span className="mr-3 inline-flex h-5 w-5 animate-spin rounded-full border-2 border-white border-t-transparent" />
              Analyzing...
            </>
          ) : (
            'Analyze Resume'
          )}
        </button>
      </form>
    </section>
  );
}

export default UploadForm;
