import React, { useState } from 'react';
import './index.css';

const App = () => {
  const [expression, setExpression] = useState('');
  const [result, setResult] = useState('');
  const [history, setHistory] = useState([]);
  const [isDarkMode, setIsDarkMode] = useState(true);

  const appendToExpression = (value) => {
    setExpression((prev) => prev + value);
  };

  const clearExpression = () => {
    setExpression('');
    setResult('');
  };

  const calculate = async () => {
    console.log('Sending request to (raw):', expression);
    // Заменяем ^ на ** перед отправкой
    const processedExpression = expression.replace(/\^/g, '**');
    console.log('Sending request to (processed):', processedExpression);
    try {
      const response = await fetch('http://localhost:8000/calculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expression: processedExpression }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}, Message: ${await response.text()}`);
      }

      const data = await response.json();
      console.log('Response:', data);
      setResult(data.result);
      setHistory((prev) => [...prev, { expression, result: data.result }].slice(-5));
    } catch (error) {
      console.error('Calculation error:', error);
      setResult(`Error: ${error.message}`);
    }
  };

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
    document.body.classList.toggle('dark');
  };

  const selectHistory = (histExpression) => {
    setExpression(histExpression);
    setResult('');
  };

  const buttons = [
    { label: 'C', action: clearExpression, className: 'bg-gradient-to-br from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white' },
    { label: '(', action: () => appendToExpression('('), className: 'bg-gradient-to-br from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white' },
    { label: ')', action: () => appendToExpression(')'), className: 'bg-gradient-to-br from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white' },
    { label: '÷', action: () => appendToExpression('/'), className: 'bg-gradient-to-br from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white' },
    { label: '7', action: () => appendToExpression('7'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '8', action: () => appendToExpression('8'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '9', action: () => appendToExpression('9'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '×', action: () => appendToExpression('*'), className: 'bg-gradient-to-br from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white' },
    { label: '4', action: () => appendToExpression('4'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '5', action: () => appendToExpression('5'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '6', action: () => appendToExpression('6'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '−', action: () => appendToExpression('-'), className: 'bg-gradient-to-br from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white' },
    { label: '1', action: () => appendToExpression('1'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '2', action: () => appendToExpression('2'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '3', action: () => appendToExpression('3'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '+', action: () => appendToExpression('+'), className: 'bg-gradient-to-br from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white' },
    { label: '0', action: () => appendToExpression('0'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white col-span-2' },
    { label: '.', action: () => appendToExpression('.'), className: 'bg-gradient-to-br from-gray-500 to-gray-600 hover:from-gray-600 hover:to-gray-700 text-white' },
    { label: '=', action: calculate, className: 'bg-gradient-to-br from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white' },
    { label: 'sin', action: () => appendToExpression('sin('), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: 'cos', action: () => appendToExpression('cos('), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: 'tan', action: () => appendToExpression('tan('), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: '√', action: () => appendToExpression('sqrt('), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: '∫', action: () => appendToExpression('∫('), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: 'π', action: () => appendToExpression('pi'), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: 'x', action: () => appendToExpression('x'), className: 'bg-gradient-to-br from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white' },
    { label: ',', action: () => appendToExpression(','), className: 'bg-gradient-to-br from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white' },
    { label: '^', action: () => appendToExpression('^'), className: 'bg-gradient-to-br from-orange-500 to-orange-600 hover:from-orange-600 hover:to-orange-700 text-white' },
  ];

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#1a1a1a] dark:bg-gray-100 transition-colors duration-500 p-4">
      <div className="w-full max-w-sm bg-[#2a2a2a] dark:bg-white/90 rounded-3xl shadow-2xl p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-bold text-white dark:text-gray-900 tracking-tight">Calculator</h1>
          <button
            onClick={toggleTheme}
            className="p-2 rounded-full bg-gray-600/50 dark:bg-gray-300/50 text-white dark:text-gray-900 hover:bg-gray-700/50 dark:hover:bg-gray-400/50 transition-colors duration-200"
            aria-label="Toggle theme"
          >
            {isDarkMode ? '☀️' : '🌙'}
          </button>
        </div>
        <div className="mb-6 bg-[#3a3a3a] dark:bg-gray-200 rounded-xl p-4 shadow-inner">
          <input
            type="text"
            value={expression}
            onChange={(e) => setExpression(e.target.value)}
            placeholder="0"
            className={`w-full bg-transparent text-3xl font-mono text-white dark:text-gray-900 focus:outline-none placeholder-gray-400 transition-colors duration-200 text-right ${result.startsWith('Error') ? 'text-red-400' : ''}`}
            style={{ minHeight: '2.5rem' }}
          />
          <div className="mt-1 text-xl font-mono text-gray-400 dark:text-gray-600 text-right">
            {result && <span>{result}</span>}
          </div>
        </div>
        <div className="grid grid-cols-4 gap-2 mb-6">
          {buttons.slice(0, 20).map((btn, idx) => (
            <button
              key={idx}
              onClick={btn.action}
              className={`p-4 rounded-xl text-lg font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 active:scale-95 transition-all duration-200 ${btn.className}`}
            >
              {btn.label}
            </button>
          ))}
        </div>
        <div className="grid grid-cols-5 gap-2 mb-6">
          {buttons.slice(20).map((btn, idx) => (
            <button
              key={idx}
              onClick={btn.action}
              className={`p-3 rounded-xl text-base font-semibold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 active:scale-95 transition-all duration-200 ${btn.className}`}
            >
              {btn.label}
            </button>
          ))}
        </div>
        <div className="bg-[#3a3a3a] dark:bg-gray-200 rounded-xl p-4 shadow-inner">
          <h2 className="text-base font-semibold text-white dark:text-gray-900 mb-2">History</h2>
          <ul className="text-sm text-gray-400 dark:text-gray-600 space-y-2 max-h-24 overflow-y-auto">
            {history.length === 0 ? (
              <li className="text-gray-500 dark:text-gray-400">No calculations yet</li>
            ) : (
              history.map((item, idx) => (
                <li
                  key={idx}
                  className="cursor-pointer hover:bg-gray-600/30 dark:hover:bg-gray-300/30 p-2 rounded-lg transition-colors duration-200"
                  onClick={() => selectHistory(item.expression)}
                >
                  {item.expression} = {item.result}
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default App;