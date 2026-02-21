import { Download } from "lucide-react";

export default function ExampleDownload() {
  return (
    <div className="mb-4 flex items-center gap-4 flex-wrap">
      <a
        href={`${import.meta.env.BASE_URL}example_template.xlsx`}
        download
        className="inline-flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md text-gray-700 transition-colors"
      >
        <Download size={16} />
        Example XLSX (from DataShop @CMU)
      </a>
      <details className="text-sm text-gray-500">
        <summary className="cursor-pointer hover:text-gray-700">
          XLSX structure
        </summary>
        <ul className="mt-1 ml-4 list-disc">
          <li>AnonStudentId: text</li>
          <li>First Attempt: correct, incorrect, hint, unknown</li>
          <li>Corrects: Positive number</li>
          <li>Incorrects: Positive number</li>
          <li>Hints: Positive number</li>
          <li>Opportunity: Positive number</li>
          <li>KC (Default): text</li>
        </ul>
      </details>
    </div>
  );
}
