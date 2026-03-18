import { useState } from 'react';
import { generatePost } from '../services/apiService';
import './GenerateContent.css';

export default function GenerateContent() {
  const [topic, setTopic] = useState('');
  const [platform, setPlatform] = useState('LinkedIn');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAction = async () => {
    if (!topic) return alert("Please enter a topic");
    setLoading(true);
    try {
      const content = await generatePost(topic, platform);
      setResult(content);
    } catch (err) {
      setResult("Error:",err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setTopic('');
    setResult('');
  };

  return (
    <div className="main-wrapper">
      <div className={`content-container ${result ? 'parallel' : ''}`}>
      
        <div className="glass-card">
          <h1 className="app-title">AI Content Generator</h1>
          
          <div className="input-group">
          <label>Topic</label>
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
              <span className="platform-tag">{platform}</span>
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