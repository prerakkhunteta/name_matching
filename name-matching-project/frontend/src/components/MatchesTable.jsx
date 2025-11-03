import React, { useState } from 'react';
import './MatchesTable.css';

const MatchesTable = ({ matches }) => {
    const [expandedRow, setExpandedRow] = useState(null);
    const [searchTerm, setSearchTerm] = useState('');

    const handleToggleDetails = (index) => {
        setExpandedRow(expandedRow === index ? null : index);
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredMatches = matches.filter(match => {
        const searchTermLower = searchTerm.toLowerCase();
        if (!searchTerm) return true;

        // Create a string with all record data to search through
        const matchDataString = `
            ${match.id1} ${match.id2} 
            ${JSON.stringify(match.record1)} 
            ${JSON.stringify(match.record2)}
        `.toLowerCase();

        return matchDataString.includes(searchTermLower);
    });

    if (!matches || matches.length === 0) {
        return <p>No matches found.</p>;
    }

    return (
        <div className="matches-table-container">
            <input
                type="text"
                placeholder="Search by ID or any record value..."
                value={searchTerm}
                onChange={handleSearchChange}
                style={{ width: '100%', padding: '10px', marginBottom: '20px', boxSizing: 'border-box' }}
            />
            <table className="matches-table">
                <thead>
                    <tr>
                        <th>Match</th>
                        <th>Similarity</th>
                        <th>Record ID 1</th>
                        <th>Record ID 2</th>
                        <th>Details</th>
                    </tr>
                </thead>
                <tbody>
                    {filteredMatches.map((match, index) => (
                        <React.Fragment key={index}>
                            <tr className="match-row">
                                <td>{index + 1}</td>
                                <td>{match.similarity_score.toFixed(2)}</td>
                                <td>{match.id1}</td>
                                <td>{match.id2}</td>
                                <td>
                                    <button onClick={() => handleToggleDetails(index)} className="details-button">
                                        {expandedRow === index ? 'Hide' : 'Show'}
                                    </button>
                                </td>
                            </tr>
                            {expandedRow === index && (
                                <tr className="details-row">
                                    <td colSpan="5">
                                        <div className="details-content">
                                            <h4>Column-wise Comparison</h4>
                                            {Object.keys(match.record1).map(col => {
                                                const val1 = String(match.record1[col]);
                                                const val2 = String(match.record2[col]);
                                                const areDifferent = val1.toLowerCase() !== val2.toLowerCase();
                                                return (
                                                    <div key={col} className="column-comparison">
                                                        <div className="column-name">{col}</div>
                                                        <div className={`column-values ${areDifferent ? 'different' : 'similar'}`}>
                                                            <span className="value1">{val1}</span>
                                                            <span className="separator">|</span>
                                                            <span className="value2">{val2}</span>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </td>
                                </tr>
                            )}
                        </React.Fragment>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default MatchesTable;