export default function LoadingOverlay() {
  return (
    <div className="flex items-center gap-3 p-4 mb-4 bg-blue-50 rounded-lg border border-blue-200">
      <div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full" />
      <span className="text-blue-700">Training models... This may take a moment.</span>
    </div>
  );
}
