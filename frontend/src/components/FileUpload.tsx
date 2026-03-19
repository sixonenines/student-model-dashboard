import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, FileCheck } from "lucide-react";

interface Props {
  onFileAccepted: (file: File) => void;
  fileName?: string | null;
}

export default function FileUpload({ onFileAccepted, fileName }: Props) {
  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted.length > 0) {
        onFileAccepted(accepted[0]);
      }
    },
    [onFileAccepted]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
    },
    maxFiles: 1,
  });

  const hasFile = !!fileName;

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors mb-4 ${
        isDragActive
          ? "border-blue-500 bg-blue-50"
          : hasFile
            ? "border-green-400 bg-green-50 hover:border-green-500"
            : "border-gray-300 hover:border-gray-400"
      }`}
    >
      <input {...getInputProps()} />
      {hasFile ? (
        <>
          <FileCheck className="mx-auto mb-2 text-green-500" size={32} />
          <p className="text-green-700 font-medium">{fileName}</p>
          <p className="text-sm text-gray-400 mt-1">
            Click or drop a new file to replace
          </p>
        </>
      ) : (
        <>
          <Upload className="mx-auto mb-2 text-gray-400" size={32} />
          {isDragActive ? (
            <p className="text-blue-600">Drop the XLSX file here...</p>
          ) : (
            <p className="text-gray-600">
              Drag &amp; drop an XLSX file here, or click to select
            </p>
          )}
          <p className="text-sm text-gray-400 mt-1">
            Required columns: AnonStudentId, First Attempt, Corrects, Incorrects,
            Opportunity, Hints, KC (Default)
          </p>
        </>
      )}
    </div>
  );
}
