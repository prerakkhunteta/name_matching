import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = ({ onMatchesReceived, onError, onLoading }) => {
    const [db1File, setDb1File] = useState(null);
    const [db2File, setDb2File] = useState(null);
    const [threshold, setThreshold] = useState(80);
    const [blockingStrategy, setBlockingStrategy] = useState('metaphone');

    const handleFile1Change = (e) => {
        setDb1File(e.target.files[0]);
    };

    const handleFile2Change = (e) => {
        setDb2File(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!db1File || !db2File) {
            onError('Please select both CSV files');
            return;
        }

        // Validate file types
        if (!db1File.name.endsWith('.csv') || !db2File.name.endsWith('.csv')) {
            onError('Please select valid CSV files');
            return;
        }

        onLoading(true);
        onError(null);

        try {
            const formData = new FormData();
            formData.append('db1_file', db1File);
            formData.append('db2_file', db2File);
            formData.append('threshold', threshold);
            formData.append('blocking', blockingStrategy);

            const response = await axios.post('/match', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            if (response.data && response.data.matches) {
                onMatchesReceived(response.data.matches);
            } else {
                onError('No matches found or invalid response format');
            }
        } catch (error) {
            console.error('Error during file upload:', error);
            if (error.response) {
                onError(`Server error: ${error.response.data.detail || error.response.statusText}`);
            } else if (error.request) {
                onError('Network error: Could not connect to server');
            } else {
                onError(`Error: ${error.message}`);
            }
        } finally {
            onLoading(false);
        }
    };

    return (
        <div className="file-upload-container">
            <h2>📁 Upload CSV Files for Duplicate Detection</h2>
            <p className="upload-description">
                Upload two CSV files and our system will automatically detect duplicates by comparing all columns.
                Perfect for finding records where names might be slightly different but other data matches.
            </p>

            <form onSubmit={handleSubmit} className="upload-form">
                <div className="file-input-group">
                    <label htmlFor="db1-file">Database 1 CSV:</label>
                    <input
                        type="file"
                        id="db1-file"
                        accept=".csv"
                        onChange={handleFile1Change}
                        required
                    />
                    {db1File && <span className="file-name">✓ {db1File.name}</span>}
                </div>

                <div className="file-input-group">
                    <label htmlFor="db2-file">Database 2 CSV:</label>
                    <input
                        type="file"
                        id="db2-file"
                        accept=".csv"
                        onChange={handleFile2Change}
                        required
                    />
                    {db2File && <span className="file-name">✓ {db2File.name}</span>}
                </div>

                <div className="settings-group">
                    <div className="setting-item">
                        <label htmlFor="threshold">Similarity Threshold (%):</label>
                        <input
                            type="number"
                            id="threshold"
                            value={threshold}
                            onChange={(e) => setThreshold(Number(e.target.value))}
                            min="50"
                            max="100"
                            step="5"
                        />
                        <small>Higher threshold = More strict matching</small>
                    </div>

                    <div className="setting-item">
                        <label htmlFor="blocking">Blocking Strategy:</label>
                        <select
                            id="blocking"
                            value={blockingStrategy}
                            onChange={(e) => setBlockingStrategy(e.target.value)}
                        >
                            <option value="metaphone">Metaphone (Phonetic)</option>
                            <option value="first_char">First Character</option>
                            <option value="length">Length-based</option>
                            <option value="soundex">Soundex</option>
                        </select>
                        <small>Strategy to group similar records for comparison</small>
                    </div>
                </div>

                <button type="submit" className="submit-button">
                    🔍 Find Duplicates
                </button>
            </form>
        </div>
    );
};

export default FileUpload;
