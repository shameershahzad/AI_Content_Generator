import { useState } from 'react';
import { generatePost } from '../services/apiService';
import './GenerateContent.css';

export default function GenerateContent() {
  const [topic, setTopic] = useState('');
  const [platform, setPlatform] = useState('LinkedIn');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleAction = async () => {
    if (!topic) return alert("Please enter a topic");
    setLoading(true);
    try {
      const content = await generatePost(topic, platform);
      setResult(content);
    } catch (err) {
      setResult(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setTopic('');
    setResult('');
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="main-wrapper">
      <div className={`content-container ${result ? 'parallel' : ''}`}>
      
        <div className="glass-card">
          <h1 className="app-title">AI Content Generator</h1>
          
          <div className="input-group">
          <label>Topic:</label>
            <textarea 
              className="input-field textarea-field"
              placeholder="Describe your topic." 
              value={topic} 
              onChange={(e) => setTopic(e.target.value)} 
              rows="4" />
          </div>

          <div className="input-group">
            <label>Platform:</label>
            <select className="select-field" value={platform} onChange={(e) => setPlatform(e.target.value)}>
              <option>LinkedIn</option>
              <option>Instagram</option>
              <option>Youtube</option>
              <option>Meta</option>
            </select>
          </div>

          <div className="button-group">
            <button className="submit-btn" onClick={handleAction} disabled={loading}>
              {loading ? "Generating..." : "Generate Post ✨"}
            </button>
            {result && <button className="clear-btn" onClick={handleClear}>Clear</button>}
          </div>
        </div>

        {result && (
          <div className="result-card fade-in">
            <div className="result-header">
              <span>PROCESSED OUTPUT</span>
              <div className="result-header-actions">
                <span className="platform-tag">{platform}</span>
                <button
                  className="copy-btn"
                  onClick={handleCopy}
                  title={copied ? 'Copied!' : 'Copy to clipboard'}
                  aria-label="Copy generated content"
                >
                  {copied ? (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="20 6 9 17 4 12" />
                    </svg>
                  ) : (
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="9" y="9" width="13" height="13" rx="2" ry="2" />
                      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                    </svg>
                  )}
                </button>
              </div>
            </div>
            <div className="result-body">
              <pre>{result}</pre>
            </div>
          </div>
        )}
        
      </div>
    </div>
  );
}