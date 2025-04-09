import { useState } from 'react';
import { questions } from '../../services/api';
import { useAuth } from '../../context/AuthContext';

export default function QuestionItem({ question }) {
  const [answers, setAnswers] = useState([]);
  const [showAnswers, setShowAnswers] = useState(false);
  const [newAnswer, setNewAnswer] = useState('');
  const { user } = useAuth();

  const handleShowAnswers = async () => {
    if (!showAnswers) {
      try {
        const response = await questions.getAnswers(question.id);
        setAnswers(response.data.results);
      } catch (error) {
        console.error('Error fetching answers:', error);
      }
    }
    setShowAnswers(!showAnswers);
  };

  const handleSubmitAnswer = async (e) => {
    e.preventDefault();
    if (!newAnswer.trim()) return;

    try {
      const response = await questions.createAnswer(question.id, { text: newAnswer });
      setAnswers([response.data, ...answers]);
      setNewAnswer('');
    } catch (error) {
      console.error('Error submitting answer:', error);
    }
  };

  const handleLikeAnswer = async (answerId) => {
    if (!user) return;

    try {
      await questions.likeAnswer(answerId, question.id);
      const response = await questions.getAnswers(question.id);
      setAnswers(response.data.results);
    } catch (error) {
      console.error('Error liking answer:', error);
    }
  };

  return (
    <div className="bg-white shadow rounded-lg mb-6 p-6">
      <div className="mb-4">
        <h2 className="text-xl font-semibold">{question.title}</h2>
        <p className="text-gray-600 mt-2">{question.text}</p>
        <div className="text-sm text-gray-500 mt-2">
          Asked by {question.author.username} on {new Date(question.created_at).toLocaleDateString()}
        </div>
      </div>

      <button
        onClick={handleShowAnswers}
        className="text-indigo-600 hover:text-indigo-800"
      >
        {showAnswers ? 'Hide' : 'Show'} {question.answers_count} Answers
      </button>

      {showAnswers && (
        <div className="mt-4">
          {user && (
            <form onSubmit={handleSubmitAnswer} className="mb-4">
              <textarea
                value={newAnswer}
                onChange={(e) => setNewAnswer(e.target.value)}
                className="w-full p-2 border rounded"
                placeholder="Write your answer..."
                rows="3"
              />
              <button
                type="submit"
                className="mt-2 bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700"
              >
                Submit Answer
              </button>
            </form>
          )}

          {answers.map((answer) => (
            <div key={answer.id} className="border-t py-4">
              <p>{answer.text}</p>
              <div className="flex items-center justify-between mt-2">
                <div className="text-sm text-gray-500">
                  By {answer.author.username} on {new Date(answer.created_at).toLocaleDateString()}
                </div>
                <button
                  onClick={() => handleLikeAnswer(answer.id)}
                  className={`flex items-center ${
                    user ? 'text-indigo-600 hover:text-indigo-800' : 'text-gray-400'
                  }`}
                  disabled={!user}
                >
                  <span className="mr-1">👍</span>
                  {answer.likes_count}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}