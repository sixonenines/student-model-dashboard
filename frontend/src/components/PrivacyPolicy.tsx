import { ArrowLeft, ExternalLink } from "lucide-react";

interface Props {
  onBack: () => void;
}

const UDE_PRIVACY_URL = "https://www.uni-due.de/en/privacy-policy.php";

export default function PrivacyPolicy({ onBack }: Props) {
  return (
    <div className="max-w-3xl mx-auto px-4 py-8">
      <button
        onClick={onBack}
        className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800 mb-6"
      >
        <ArrowLeft size={16} />
        Back to Dashboard
      </button>

      <h1 className="text-3xl font-bold text-gray-900 mb-2">Privacy Policy</h1>
      <p className="text-sm text-gray-400 mb-8">Last updated: March 2026</p>

      <div className="space-y-6 text-gray-700 text-sm leading-relaxed">
        <section className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p>
            This platform is operated within the University of Duisburg-Essen
            (UDE). The general{" "}
            <a
              href={UDE_PRIVACY_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 underline inline-flex items-center gap-1"
            >
              UDE privacy policy
              <ExternalLink size={12} />
            </a>{" "}
            and data management policies apply. The information below describes
            additional, platform-specific processing.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            1. Controller and Data Protection Officer
          </h2>
          <p>
            The controller (responsible entity) and the UDE Data Protection
            Officer (DPO) are listed in the{" "}
            <a
              href={UDE_PRIVACY_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              UDE privacy policy
            </a>
            .
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            2. What This Platform Does
          </h2>
          <p>
            The IRT Student Models Dashboard is a research tool developed as
            part of a bachelor thesis project. It allows users to upload
            educational data (XLSX files) and train Item Response Theory (IRT)
            statistical models. Results are computed on the server and returned
            to the browser for download.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            3. What Data We Process on This Platform
          </h2>
          <p>
            When you use this platform, the following data is processed:
          </p>
          <ul className="list-disc pl-5 mt-2 space-y-1">
            <li>
              <strong>Uploaded files:</strong> The XLSX file you upload,
              containing educational data (student IDs, attempt counts,
              correctness scores, hints, and knowledge component labels).
            </li>
            <li>
              <strong>Server logs:</strong> Standard web server access logs
              (IP address, timestamp, request path) may be recorded for
              operational purposes.
            </li>
          </ul>
          <p className="mt-2">
            We do not use cookies, tracking scripts, or analytics services.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            4. Cookies / Local Storage / Client-Side Caching
          </h2>
          <p>
            This platform does not set cookies, use local storage, or cache
            any user data on the client side. All processing results are
            delivered directly and are not persisted in the browser.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            5. Purpose and Legal Basis
          </h2>
          <p>
            Your uploaded file is processed solely to train the statistical
            models you select. The legal basis for this processing is your
            consent (Art. 6(1)(a) GDPR), which you provide by voluntarily
            uploading a file. No data is processed until you initiate the
            upload.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            6. Data Sharing
          </h2>
          <p>
            Your data is not shared with, sold to, or made accessible to any
            third parties. All processing occurs exclusively on the server
            hosting this platform.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            7. Retention
          </h2>
          <p>
            Uploaded files are held in server memory only for the duration of
            the model training request. Once processing is complete (or if an
            error occurs), the file data is automatically discarded. No
            uploaded data is written to persistent storage, databases, or
            backups.
          </p>
        </section>

        <section>
          <h2 className="text-lg font-semibold text-gray-900 mb-2">
            8. Your Rights and Contact
          </h2>
          <p>
            Data subject rights and contact routes (including the UDE Data
            Protection Officer and supervisory authority information) are
            described in the{" "}
            <a
              href={UDE_PRIVACY_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 underline"
            >
              UDE privacy policy
            </a>
            .
          </p>
        </section>
      </div>
    </div>
  );
}
