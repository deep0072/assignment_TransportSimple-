import { useState, useEffect } from 'react';
import { questions } from '../../services/api';
import QuestionItem from './QuestionItem';

export default function QuestionList() {
  const [questionsList, setQuestionsList] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await questions.getAll();
        setQuestionsList(response.data.results);
      } catch (error) {
        console.error('Error fetching questions:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchQuestions();
  }, []);

  if (loading) {
    return <div className="text-center py-4">Loading...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto py-8">
      {questionsList.map((question) => (
        <QuestionItem key={question.id} question={question} />
      ))}
    </div>
  );
}