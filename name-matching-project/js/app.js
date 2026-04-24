let currentOldPatient = null;
let currentIdType = 'aadhaar';

const database = {
    aadhaar: {
        '234567890123': { name: 'Ramesh Kumar Sharma', dob: '1985-03-14', gender: 'Male', father: 'Suresh Kumar Sharma', address: 'Flat 12 Gandhi Nagar Jaipur', state: 'Rajasthan', phone: '9876543210', email: 'ramesh.sharma@email.com' },
        '345678901234': { name: 'Priya Nair', dob: '1992-07-22', gender: 'Female', father: 'Krishnan Nair', address: 'House 45 MG Road Kochi', state: 'Kerala', phone: '9876543211', email: 'priya.nair@email.com' },
        '456789012345': { name: 'Mohammad Ali Khan', dob: '1978-11-05', gender: 'Male', father: 'Abdul Khan', address: 'Plot 7 Civil Lines Lucknow', state: 'Uttar Pradesh', phone: '9876543212', email: 'ali.khan@email.com' },
        '567890123456': { name: 'Sunita Devi', dob: '1990-01-30', gender: 'Female', father: 'Rajesh Kumar', address: 'House 3 Station Road Patna', state: 'Bihar', phone: '9876543213', email: 'sunita.devi@email.com' },
        '678901234567': { name: 'Arjun Singh Mehta', dob: '1983-09-18', gender: 'Male', father: 'Vikram Singh Mehta', address: 'Flat 88 Ring Road Ahmedabad', state: 'Gujarat', phone: '9876543214', email: 'arjun.mehta@email.com' },
        '789012345678': { name: 'Anjali Venkat Reddy', dob: '1995-06-25', gender: 'Female', father: 'Venkat Reddy', address: 'Banjara Hills Hyderabad', state: 'Telangana', phone: '9876543215', email: 'anjali.reddy@email.com' },
        '890123456789': { name: 'Rajesh Kumar Verma', dob: '1988-12-10', gender: 'Male', father: 'Prakash Verma', address: 'Sector 21 Noida', state: 'Uttar Pradesh', phone: '9876543216', email: 'rajesh.verma@email.com' },
        '901234567890': { name: 'Kavita Patel', dob: '1991-04-18', gender: 'Female', father: 'Ramesh Patel', address: 'Satellite Ahmedabad', state: 'Gujarat', phone: '9876543217', email: 'kavita.patel@email.com' },
        '012345678901': { name: 'Vikram Malhotra', dob: '1987-08-22', gender: 'Male', father: 'Sunil Malhotra', address: 'Defence Colony Delhi', state: 'Delhi', phone: '9876543218', email: 'vikram.malhotra@email.com' },
        '123450987654': { name: 'Meera Subramanian Iyer', dob: '1993-11-15', gender: 'Female', father: 'Subramanian Iyer', address: 'T Nagar Chennai', state: 'Tamil Nadu', phone: '9876543219', email: 'meera.iyer@email.com' }
    },
    pan: {
        'ABCDE1234F': { name: 'Ramesh K Sharma', dob: '1985-03-14', gender: 'Male', father: 'Suresh Kumar Sharma', address: 'Flat 12 Gandhi Nagar Jaipur', state: 'Rajasthan', phone: '9876543210', email: 'ramesh.sharma@email.com' },
        'BCDEF2345G': { name: 'Priya Nayr', dob: '1992-07-22', gender: 'Female', father: 'Krishnan Nair', address: 'House 45 MG Road Kochi', state: 'Kerala', phone: '9876543211', email: 'priya.nair@email.com' },
        'CDEFG3456H': { name: 'Mohammad Ali Khan', dob: '1978-11-05', gender: 'Male', father: 'Abdul Khan', address: 'Plot 7 Civil Lines Lucknow', state: 'Uttar Pradesh', phone: '9876543212', email: 'ali.khan@email.com' },
        'DEFGH4567I': { name: 'Sunita Devi', dob: '1990-01-30', gender: 'Female', father: 'Rajesh Kumar', address: 'House 3 Station Road Patna', state: 'Bihar', phone: '9876543213', email: 'sunita.devi@email.com' },
        'EFGHI5678J': { name: 'Arjun S Mehta', dob: '1983-09-18', gender: 'Male', father: 'Vikram Singh Mehta', address: 'Flat 88 Ring Road Ahmedabad', state: 'Gujarat', phone: '9876543214', email: 'arjun.mehta@email.com' },
        'FGHIJ6789K': { name: 'Anjali V Reddy', dob: '1995-06-25', gender: 'Female', father: 'Venkat Reddy', address: 'Banjara Hills Hyderabad', state: 'Telangana', phone: '9876543215', email: 'anjali.reddy@email.com' },
        'GHIJK7890L': { name: 'Rajesh K Verma', dob: '1988-12-10', gender: 'Male', father: 'Prakash Verma', address: 'Sector 21 Noida', state: 'Uttar Pradesh', phone: '9876543216', email: 'rajesh.verma@email.com' },
        'HIJKL8901M': { name: 'Kavita Patel', dob: '1991-04-18', gender: 'Female', father: 'Ramesh Patel', address: 'Satellite Ahmedabad', state: 'Gujarat', phone: '9876543217', email: 'kavita.patel@email.com' },
        'IJKLM9012N': { name: 'V Malhotra', dob: '1987-08-22', gender: 'Male', father: 'Sunil Malhotra', address: 'Defence Colony Delhi', state: 'Delhi', phone: '9876543218', email: 'vikram.malhotra@email.com' },
        'JKLMN0123O': { name: 'Meera S Iyer', dob: '1993-11-15', gender: 'Female', father: 'Subramanian Iyer', address: 'T Nagar Chennai', state: 'Tamil Nadu', phone: '9876543219', email: 'meera.iyer@email.com' }
    },
    voter: {
        'RJ1234567890': { name: 'Ramesh Kumar Sharma', dob: '1985-03-14', gender: 'Male', father: 'Suresh Kumar Sharma', address: 'Flat 12 Gandhi Nagar Jaipur', state: 'Rajasthan', phone: '9876543210', email: 'ramesh.sharma@email.com' },
        'KL2345678901': { name: 'Priya Nair', dob: '1992-07-22', gender: 'Female', father: 'Krishnan Nair', address: 'House 45 MG Road Kochi', state: 'Kerala', phone: '9876543211', email: 'priya.nair@email.com' },
        'UP3456789012': { name: 'Mohammed Ali Khan', dob: '1978-11-05', gender: 'Male', father: 'Abdul Khan', address: 'Plot 7 Civil Lines Lucknow', state: 'Uttar Pradesh', phone: '9876543212', email: 'ali.khan@email.com' },
        'BR4567890123': { name: 'Sunita Devi', dob: '1990-01-30', gender: 'Female', father: 'Rajesh Kumar', address: 'House 3 Station Road Patna', state: 'Bihar', phone: '9876543213', email: 'sunita.devi@email.com' },
        'GJ5678901234': { name: 'Arjun Mehta', dob: '1983-09-18', gender: 'Male', father: 'Vikram Singh Mehta', address: 'Flat 88 Ring Road Ahmedabad', state: 'Gujarat', phone: '9876543214', email: 'arjun.mehta@email.com' },
        'TG6789012345': { name: 'Anjali Reddy', dob: '1995-06-25', gender: 'Female', father: 'Venkat Reddy', address: 'Banjara Hills Hyderabad', state: 'Telangana', phone: '9876543215', email: 'anjali.reddy@email.com' },
        'UP7890123456': { name: 'Rajesh Verma', dob: '1988-12-10', gender: 'Male', father: 'Prakash Verma', address: 'Sector 21 Noida', state: 'Uttar Pradesh', phone: '9876543216', email: 'rajesh.verma@email.com' },
        'GJ8901234567': { name: 'Kavita Patel', dob: '1991-04-18', gender: 'Female', father: 'Ramesh Patel', address: 'Satellite Ahmedabad', state: 'Gujarat', phone: '9876543217', email: 'kavita.patel@email.com' },
        'DL9012345678': { name: 'Vikram Malhotra', dob: '1987-08-22', gender: 'Male', father: 'Sunil Malhotra', address: 'Defence Colony Delhi', state: 'Delhi', phone: '9876543218', email: 'vikram.malhotra@email.com' },
        'TN0123456789': { name: 'Meera Iyer', dob: '1993-11-15', gender: 'Female', father: 'Subramanian Iyer', address: 'T Nagar Chennai', state: 'Tamil Nadu', phone: '9876543219', email: 'meera.iyer@email.com' }
    }
};

function showPage(pageId) {
    document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
    document.getElementById(pageId).classList.add('active');
    
    document.querySelectorAll('.nav-links a').forEach(link => link.classList.remove('active'));
    event.target.classList.add('active');
}

function selectIdType(type) {
    currentIdType = type;
    document.querySelectorAll('.id-type-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
    
    const input = document.getElementById('idInput');
    const sampleIds = document.getElementById('sampleIds');
    
    const placeholders = {
        aadhaar: 'Enter 12-digit Aadhaar number (e.g., 234567890123)',
        pan: 'Enter PAN number (e.g., ABCDE1234F)',
        voter: 'Enter Voter ID (e.g., RJ1234567890)'
    };
    
    const samples = {
        aadhaar: ['234567890123', '345678901234', '456789012345'],
        pan: ['ABCDE1234F', 'BCDEF2345G', 'CDEFG3456H'],
        voter: ['RJ1234567890', 'KL2345678901', 'UP3456789012']
    };
    
    input.placeholder = placeholders[type];
    input.value = '';
    
    sampleIds.innerHTML = samples[type].map(id => 
        `<span class="sample-id" onclick="tryId('${id}')">${id}</span>`
    ).join('');
}

function tryId(id) {
    document.getElementById('idInput').value = id;
}

function fetchRecord() {
    const idInput = document.getElementById('idInput').value.trim();
    if (!idInput) {
        alert('Please enter an ID number');
        return;
    }

    clearFormFields();
    hideDuplicateWarning();

    document.getElementById('statusField').value = 'Fetching from database...';

    setTimeout(() => {
        const record = database[currentIdType][idInput];
        
        if (record) {
            fillFormField('nameField', record.name, 'nameTag');
            fillFormField('fatherField', record.father, 'fatherTag');
            fillFormField('dobField', record.dob, 'dobTag');
            fillFormField('genderField', record.gender, 'genderTag');
            fillFormField('addressField', record.address, 'addressTag');
            fillFormField('stateField', record.state, 'stateTag');
            fillFormField('phoneField', record.phone, 'phoneTag');
            fillFormField('emailField', record.email, 'emailTag');
            
            document.getElementById('sourceField').value = currentIdType.toUpperCase() + ' Database';
            document.getElementById('sourceField').classList.add('filled');
            
            document.getElementById('statusField').value = '✓ Verified';
            document.getElementById('statusField').classList.add('filled');
            document.getElementById('statusField').style.color = 'var(--success)';
            document.getElementById('statusField').style.fontWeight = '600';
            
            document.getElementById('successBanner').style.display = 'block';
            
            checkForDuplicates(record.name, record.dob, record.address);
        } else {
            document.getElementById('statusField').value = '❌ Record Not Found';
            document.getElementById('statusField').style.color = 'var(--danger)';
            document.getElementById('statusField').style.fontWeight = '600';
            alert('No record found for ID: ' + idInput + '\n\nPlease try one of the sample IDs.');
        }
    }, 800);
}

async function checkForDuplicates(name, dob, address) {
    console.log('Checking for duplicates:', name, dob, address);
    try {
        const formData = new FormData();
        formData.append('name', name);
        formData.append('dob', dob);
        formData.append('address', address);
        
        const response = await fetch('http://localhost:8000/check-duplicate', {
            method: 'POST',
            body: formData
        });
        
        console.log('Backend response status:', response.status);
        
        if (!response.ok) {
            throw new Error('Backend returned error: ' + response.status);
        }
        
        const data = await response.json();
        console.log('Backend data:', data);
        
        if (data.duplicate_found) {
            showDuplicateWarning(name, data.top_match);
        } else {
            console.log('No duplicate found by backend');
        }
    } catch (error) {
        console.log('Backend error, using mock duplicate check:', error.message);
        mockDuplicateCheck(name, dob, address);
    }
}

function mockDuplicateCheck(name, dob, address) {
    console.log('Mock duplicate check called for:', name);
    const oldPatients = {
        'Mohammad Ali Khan': { 
            patient_id: 'OLD001',
            name: 'Md. Ali Khan', 
            dob: '1978-11-05',
            gender: 'Male',
            father_name: 'Abdul Khan',
            address: 'Plot 7 Civil Lines Lucknow', 
            city: 'Lucknow',
            state: 'Uttar Pradesh',
            registration_date: '2019-03-15',
            last_visit: '2024-12-10',
            name_score: 84, 
            dob_score: 100, 
            address_score: 91, 
            overall_confidence: 89 
        },
        'Ramesh Kumar Sharma': { 
            patient_id: 'OLD002',
            name: 'R Kumar Sharma', 
            dob: '1985-03-14',
            gender: 'Male',
            father_name: 'Suresh Sharma',
            address: 'Flat 12 Gandhi Nagar', 
            city: 'Jaipur',
            state: 'Rajasthan',
            registration_date: '2018-07-22',
            last_visit: '2025-01-05',
            name_score: 78, 
            dob_score: 100, 
            address_score: 88, 
            overall_confidence: 85 
        },
        'Priya Nair': { 
            patient_id: 'OLD003',
            name: 'Priya Nayr', 
            dob: '1992-07-22',
            gender: 'Female',
            father_name: 'K Nair',
            address: 'House 45 MG Road', 
            city: 'Kochi',
            state: 'Kerala',
            registration_date: '2020-01-10',
            last_visit: '2025-02-14',
            name_score: 92, 
            dob_score: 100, 
            address_score: 95, 
            overall_confidence: 94 
        },
        'Arjun Singh Mehta': { 
            patient_id: 'OLD005',
            name: 'Arjun Mehta', 
            dob: '1983-09-18',
            gender: 'Male',
            father_name: 'Vikram Mehta',
            address: 'Flat 88 Ring Road', 
            city: 'Ahmedabad',
            state: 'Gujarat',
            registration_date: '2021-05-12',
            last_visit: '2025-03-01',
            name_score: 81, 
            dob_score: 100, 
            address_score: 93, 
            overall_confidence: 88 
        },
        'Sunita Devi': { 
            patient_id: 'OLD004',
            name: 'Sunita Devi', 
            dob: '1990-01-30',
            gender: 'Female',
            father_name: 'Rajesh Kumar',
            address: 'House 3 Station Road', 
            city: 'Patna',
            state: 'Bihar',
            registration_date: '2019-11-20',
            last_visit: '2024-11-30',
            name_score: 100, 
            dob_score: 100, 
            address_score: 100, 
            overall_confidence: 100 
        },
        'Anjali Venkat Reddy': { 
            patient_id: 'OLD006',
            name: 'Anjali V Reddy', 
            dob: '1995-06-25',
            gender: 'Female',
            father_name: 'Venkat Reddy',
            address: 'Banjara Hills', 
            city: 'Hyderabad',
            state: 'Telangana',
            registration_date: '2020-08-30',
            last_visit: '2025-01-20',
            name_score: 87, 
            dob_score: 100, 
            address_score: 92, 
            overall_confidence: 91 
        },
        'Rajesh Kumar Verma': { 
            patient_id: 'OLD007',
            name: 'Rajesh K Verma', 
            dob: '1988-12-10',
            gender: 'Male',
            father_name: 'Prakash Verma',
            address: 'Sector 21', 
            city: 'Noida',
            state: 'Uttar Pradesh',
            registration_date: '2019-02-18',
            last_visit: '2024-10-15',
            name_score: 83, 
            dob_score: 100, 
            address_score: 89, 
            overall_confidence: 88 
        },
        'Kavita Patel': { 
            patient_id: 'OLD008',
            name: 'Kavita Patel', 
            dob: '1991-04-18',
            gender: 'Female',
            father_name: 'Ramesh Patel',
            address: 'Satellite', 
            city: 'Ahmedabad',
            state: 'Gujarat',
            registration_date: '2018-12-05',
            last_visit: '2025-02-28',
            name_score: 100, 
            dob_score: 100, 
            address_score: 100, 
            overall_confidence: 100 
        },
        'Vikram Malhotra': { 
            patient_id: 'OLD009',
            name: 'V Malhotra', 
            dob: '1987-08-22',
            gender: 'Male',
            father_name: 'Sunil Malhotra',
            address: 'Defence Colony', 
            city: 'Delhi',
            state: 'Delhi',
            registration_date: '2020-06-14',
            last_visit: '2025-01-10',
            name_score: 79, 
            dob_score: 100, 
            address_score: 86, 
            overall_confidence: 85 
        },
        'Meera Subramanian Iyer': { 
            patient_id: 'OLD010',
            name: 'Meera S Iyer', 
            dob: '1993-11-15',
            gender: 'Female',
            father_name: 'Subramanian Iyer',
            address: 'T Nagar', 
            city: 'Chennai',
            state: 'Tamil Nadu',
            registration_date: '2019-09-25',
            last_visit: '2024-12-20',
            name_score: 82, 
            dob_score: 100, 
            address_score: 90, 
            overall_confidence: 88 
        }
    };
    
    console.log('Looking for patient:', name);
    console.log('Available patients:', Object.keys(oldPatients));
    
    if (oldPatients[name]) {
        console.log('Match found!', oldPatients[name]);
        currentOldPatient = oldPatients[name];
        showDuplicateWarning(name, oldPatients[name]);
    } else {
        console.log('No match found for:', name);
    }
}

function showDuplicateWarning(newName, oldPatient) {
    currentOldPatient = oldPatient;
    
    const warningCard = document.getElementById('duplicateWarning');
    document.getElementById('newPatientName').textContent = newName;
    document.getElementById('oldPatientName').textContent = oldPatient.name;
    document.getElementById('oldPatientDob').textContent = oldPatient.dob;
    document.getElementById('oldPatientAddress').textContent = oldPatient.address;
    
    const nameScore = oldPatient.name_score || oldPatient.nameScore || 0;
    const dobScore = oldPatient.dob_score || oldPatient.dobScore || 0;
    const addressScore = oldPatient.address_score || oldPatient.addressScore || 0;
    const overallScore = oldPatient.overall_confidence || oldPatient.overall || 0;
    
    document.getElementById('nameScoreBar').style.width = nameScore + '%';
    document.getElementById('nameScoreText').textContent = nameScore + '%';
    
    document.getElementById('dobScoreBar').style.width = dobScore + '%';
    document.getElementById('dobScoreText').textContent = dobScore + '%';
    
    document.getElementById('addressScoreBar').style.width = addressScore + '%';
    document.getElementById('addressScoreText').textContent = addressScore + '%';
    
    document.getElementById('overallConfidence').textContent = overallScore + '%';
    
    let confidenceText = '';
    if (overallScore >= 90) {
        confidenceText = 'Very High — Almost certainly same person';
    } else if (overallScore >= 80) {
        confidenceText = 'High — Likely same person';
    } else {
        confidenceText = 'Medium — Possibly same person';
    }
    document.getElementById('confidenceLevel').textContent = confidenceText;
    
    warningCard.style.display = 'block';
    
    console.log('Duplicate warning shown, currentOldPatient:', currentOldPatient);
}

function hideDuplicateWarning() {
    document.getElementById('duplicateWarning').style.display = 'none';
}

function fillFormField(fieldId, value, tagId) {
    const field = document.getElementById(fieldId);
    field.value = value;
    field.classList.add('filled');
    document.getElementById(tagId).style.display = 'inline-block';
}

function clearFormFields() {
    const fields = ['nameField', 'fatherField', 'dobField', 'genderField', 'addressField', 'stateField', 'phoneField', 'emailField', 'sourceField', 'statusField'];
    const tags = ['nameTag', 'fatherTag', 'dobTag', 'genderTag', 'addressTag', 'stateTag', 'phoneTag', 'emailTag'];
    
    fields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        field.value = '';
        field.classList.remove('filled');
        field.style.color = '';
        field.style.fontWeight = '';
    });
    
    tags.forEach(tagId => {
        document.getElementById(tagId).style.display = 'none';
    });
    
    document.getElementById('successBanner').style.display = 'none';
}

function viewExistingRecord() {
    console.log('viewExistingRecord called, currentOldPatient:', currentOldPatient);
    
    if (!currentOldPatient) {
        alert('No patient data available. Please try fetching the record again.');
        return;
    }
    
    document.getElementById('modalPatientId').textContent = currentOldPatient.patient_id || 'N/A';
    document.getElementById('modalName').textContent = currentOldPatient.name || 'N/A';
    document.getElementById('modalFather').textContent = currentOldPatient.father_name || 'N/A';
    document.getElementById('modalDob').textContent = currentOldPatient.dob || 'N/A';
    document.getElementById('modalGender').textContent = currentOldPatient.gender || 'N/A';
    document.getElementById('modalAddress').textContent = currentOldPatient.address || 'N/A';
    document.getElementById('modalCity').textContent = currentOldPatient.city || 'N/A';
    document.getElementById('modalState').textContent = currentOldPatient.state || 'N/A';
    document.getElementById('modalRegDate').textContent = currentOldPatient.registration_date || 'N/A';
    document.getElementById('modalLastVisit').textContent = currentOldPatient.last_visit || 'N/A';
    
    const modal = document.getElementById('existingRecordModal');
    if (modal) {
        modal.style.display = 'block';
        console.log('Modal displayed');
    } else {
        console.error('Modal element not found!');
        alert('Error: Modal not found. Please refresh the page.');
    }
}

function closeModal() {
    document.getElementById('existingRecordModal').style.display = 'none';
}

function mergeRecords() {
    if (confirm('Merge these records?\n\nThis will link the old patient record with the new Aadhaar registration.')) {
        alert('✓ Records merged successfully!\n\nPatient ID: ' + currentOldPatient.patient_id + '\nAadhaar linked and medical history preserved.');
        closeModal();
        hideDuplicateWarning();
    }
}

function registerAsNew() {
    if (confirm('Are you sure this is a different patient?\n\nThis will create a new patient record.')) {
        alert('Patient registered as new.\n\nIn a real system, this would save to the database.');
        hideDuplicateWarning();
    }
}

window.onclick = function(event) {
    const modal = document.getElementById('existingRecordModal');
    if (event.target == modal) {
        closeModal();
    }
}
