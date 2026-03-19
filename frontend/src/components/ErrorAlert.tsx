interface Props {
  message: string;
}

export default function ErrorAlert({ message }: Props) {
  return (
    <div className="p-4 mb-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
      {message}
    </div>
  );
}
