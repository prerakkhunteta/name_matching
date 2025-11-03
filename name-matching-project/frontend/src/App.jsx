import React, { useState } from 'react';
import './App.css';
import FileUpload from './components/FileUpload';
import MatchesTable from './components/MatchesTable';

function App() {
    const [matches, setMatches] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleMatchesReceived = (matchesData) => {
        setMatches(matchesData);
        setError(null);
    };

    const handleError = (errorMessage) => {
        setError(errorMessage);
        setMatches([]);
    };

    const handleLoading = (isLoading) => {
        setLoading(isLoading);
    };

    return (
        <div className="App">
            <header className="App-header">
                <h1>🔍 Name Matching System</h1>
                <p>Upload CSV files to find matching names across datasets</p>
            </header>

            <main className="App-main">
                <FileUpload
                    onMatchesReceived={handleMatchesReceived}
                    onError={handleError}
                    onLoading={handleLoading}
                />

                {loading && (
                    <div className="loading">
                        <div className="spinner"></div>
                        <p>Processing files and finding matches...</p>
                    </div>
                )}

                {error && (
                    <div className="error">
                        <p>❌ Error: {error}</p>
                    </div>
                )}

                {matches.length > 0 && (
                    <MatchesTable matches={matches} />
                )}
            </main>

            <footer className="App-footer">
                <p>Powered by FastAPI & React • Name Matching Algorithm</p>
            </footer>
        </div>
    );
}

export default App;
