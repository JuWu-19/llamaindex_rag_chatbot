<template>
  <div>
    <h1>User Dashboard</h1>
    <p>Welcome to your Dashboard, {{ username }}!</p>

    <!-- Document Upload Section -->
    <section>
      <h2>Upload Document</h2>
      <input type="file" @change="handleFileChange" />
      <input v-model="docNameUpload" placeholder="Enter document name for upload" />
      <button @click="previewFile">Upload & Preview</button>
      <textarea v-model="uploadPreviewContent" placeholder="Preview uploaded content here"></textarea>
      <button @click="submitUploadDocument">Confirm Upload</button>
    </section>

    <!-- Web Scraping Section -->
    <section>
      <h2>Scrape Document</h2>
      <input v-model="url" @input="handleUrlChange" placeholder="Enter URL to scrape" />
      <input v-model="docNameScrape" placeholder="Enter document name for scrape" />
      <button @click="scrapeContent">Extract & Preview</button>
      <textarea v-model="scrapePreviewContent" placeholder="Preview scraped content here"></textarea>
      <button @click="submitScrapeDocument">Confirm Upload</button>
    </section>
    <!-- Document List -->
    <div class="dashboard-container">
    <div class="dashboard-documents">
      <h2>Documents</h2>
      <ul>
        <li v-for="doc in documents" :key="doc.doc_id">
          {{ doc.doc_name }} by {{ doc.uploader }} - Access: {{ doc.has_access ? 'Yes' : 'No' }}
        </li>
      </ul>
    </div>

    <div class="dashboard-chat">
    <h2>RAG Q&A</h2>
    <div class="chat-view">
      <div v-for="(chat, index) in chatHistory" :key="index" class="chat-message">
        <span class="chat-sender">{{ chat.sender }}:</span>
        <span class="chat-content">{{ chat.message }}</span>
        <span class="chat-timestamp">{{ chat.timestamp }}</span>
        <span class="chat-docs">{{ chat.accessedDocs }}</span>
        <span class="docu-rele">{{ chat.docu_rele}}</span>
      </div>
    </div>
    <input type="text" v-model="newQuery" placeholder="Message ChatGPT…" />
    <button @click="sendQueryRAG">Send</button>
    <button @click="clearChatHistory">clear chat history</button>
  </div>

  </div>
    
    <!-- Feedback Dashboard -->
  <div class="feedback-dashboard">
    <h3>Feedback</h3>
    <textarea v-model="newFeedback" placeholder="Enter your feedback..."></textarea>
    <button @click="submitFeedback">Send Feedback</button>
  </div>

    <button @click="logout">Logout</button>
  </div>
</template>

<style scoped>
.chat-view {
  height: 300px;
  overflow-y: auto;
  background-color: #f7f7f7;
  padding: 10px;
  border: 1px solid #ddd;
}
.chat-message {
  margin-bottom: 10px;
}
.chat-sender {
  font-weight: bold;
}
.chat-timestamp {
  font-size: 0.8rem;
  margin-left: 10px;
}

.user-dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.document-section {
  width: 80%;  /* Adjust width as needed */
  margin: 20px auto;
}
</style>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '', // To store the username
      userId:'',
      documents: [], // To store documents accessible to the user
      accountNumber: localStorage.getItem('cur_num') || '',
      password: localStorage.getItem('cur_pass') || '',  // Storing passwords in localStorage is generally unsafe
      file: null,
      url: '',
      uploadPreviewContent: '',
      scrapePreviewContent: '',
      docNameUpload: '',  // Document name for upload
      docNameScrape: '',  // Document name for scrape
      loginError: '', // To store login error messages

      chatHistory: [],
      newQuery: '',
      newFeedback: '',
    };
  },
  created() {
    this.fetchUserData();
  },
  methods: {
    fetchUserData() {
      axios.post('http://127.0.0.1:5000/api/get-user-data', {
        account_number: this.accountNumber,
        password: this.password
      }, {
  withCredentials: false // This should be explicitly set to false
})
      .then(response => {
        if (response.data.username) {
          this.username = response.data.username;
          this.documents = response.data.documents;
          this.userId=response.data.userID;
        } else {
          console.error('Failed to fetch user data:', response.data.error);
        }
      })
      .catch(error => {
        console.error('Error fetching user data:', error);
        // Handle errors or redirect to login if the fetch fails
      });
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
      this.uploadPreviewContent = '';  // Reset the preview content
      this.docNameUpload = '';  // Reset the document name for upload
    },
    handleUrlChange() {
      this.scrapePreviewContent = '';  // Reset the scrape preview content
      this.docNameScrape = '';  // Reset the document name for scrape
    },
    previewFile() {
      if (!this.file) {
        alert('Please select a file first.');
        return;
      }
      const reader = new FileReader();
      reader.readAsText(this.file);
      reader.onload = e => {
        this.uploadPreviewContent = e.target.result;
      };
    },
    submitUploadDocument() {
      if (!this.uploadPreviewContent || !this.docNameUpload) {
        alert('No content to upload or document name not specified. Please upload and preview a document first.');
        return;
      }
      axios.post('http://127.0.0.1:5000/api/upload', {
        content: this.uploadPreviewContent,
        docName: this.docNameUpload,
        userId: this.userId,  // Assuming user ID is stored or retrieved from session
        docKind: 1
      }, {
  withCredentials: false // This should be explicitly set to false
}).then(response => {
        console.log(response.data.message);
        this.uploadPreviewContent = ''; // Clear the preview content
        this.docNameUpload = ''; // Clear the document name input
        this.file = null;
     //   this.fetchUserDocuments();  // Refresh the document list
        this.fetchUserData();
      }).catch(error => {
        console.log(this.userId);
        console.error('Error uploading:', error.response.data);
      });
    },
    scrapeContent() {
      if (!this.url || !this.docNameScrape) {
        alert('Please enter a URL and a document name for scraping.');
        return;
      }
      axios.post('http://127.0.0.1:5000/api/scrape', {
        url: this.url,
        docName: this.docNameScrape,
        userId: this.userId,
        docKind: 0
      }, {
  withCredentials: false // This should be explicitly set to false
}).then(response => {
        console.log(response); // Log the full response
        this.scrapePreviewContent = response.data.content;
        console.log(response.data.message);
        //this.fetchUserDocuments();  // Refresh the document list
      }).catch(error => {
        console.error('Error scraping:', error.response.data);
      });
    },
    submitScrapeDocument() {
      if (!this.scrapePreviewContent || !this.docNameScrape) {
        alert('No content to upload or document name not specified. Please scrape and preview a document first.');
        return;
      }
      axios.post('http://127.0.0.1:5000/api/upload', {
        content: this.scrapePreviewContent,
        docName: this.docNameScrape,
        userId: this.userId, // Assuming user ID is stored or retrieved from session
        docKind: 0 // Assuming '0' is the kind for scraped documents
      }, {
  withCredentials: false // This should be explicitly set to false
}).then(response => {
        console.log(response.data.message);
      //  this.fetchUserDocuments(); // Refresh the document list
        this.fetchUserData();
        this.scrapePreviewContent = ''; // Clear the preview content
        this.url = '';
        this.docNameScrape = ''; // Clear the document name input
      }).catch(error => {
        console.error('Error uploading scraped document:', error.response.data);
      });
    },
    fetchUserDocuments() {
      // Implementation to fetch user-specific documents
    },

sendQuery() {
      const queryToSend = this.newQuery;
      const accessedDocuments = this.documents.filter(doc => doc.has_access).map(doc => doc.doc_name).join(', ');

      this.chatHistory.push({
            sender: this.username,
            message: queryToSend,
            timestamp: new Date().toISOString(),
            accessedDocs: accessedDocuments  // Store accessed document names here
          });
      this.newQuery = ''; // Clear input after sending

      // Send the query to the server/backend
      axios.post('http://127.0.0.1:5000/api/send-query', { query: queryToSend }, {
  withCredentials: false // This should be explicitly set to false
})
        .then(response => {
         // const { answer, timestamp } = response.data;
          console.log(response.data);
          const answer = response.data.choices[0].message.content; // Assuming the structure matches the OpenAI API response
        //  const timestamp = response.data.created; // The timestamp might need to be converted into a readable format
          const timestamp = new Date(response.data.created * 1000).toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
              });
          console.log(answer); // Now log the extracted answer
          // Update chatHistory with the user's query

          // Update chatHistory with the server's response
          this.chatHistory.push({
            sender: 'Bot',
            message: answer,
            timestamp: timestamp,
            accessedDocs:''
          });
           // Save the query-answer pair along with accessed documents
          this.saveQueryAnswerPair(this.username, queryToSend, accessedDocuments, answer, timestamp);
        })
        .catch(error => {
          console.error('Error sending query:', error);
           // Optionally, handle the error by notifying the user or adding an error message to the chat history
          this.chatHistory.push({
            sender: 'Bot',
            message: 'Error retrieving response. Please try again.',
            timestamp: new Date().toISOString()
          });
          // Handle the error, possibly by notifying the user
        });
    },
    sendQueryRAG() {
      const queryToSend = this.newQuery;
      const accessedDocuments = this.documents.filter(doc => doc.has_access).map(doc => doc.doc_name).join(', ');

      this.chatHistory.push({
            sender: this.username,
            message: queryToSend,
            timestamp: new Date().toISOString(),
            accessedDocs: accessedDocuments,  // Store accessed document names here
            docu_rele: ''
          });
      this.newQuery = ''; // Clear input after sending

      // Send the query to the server/backend
      axios.post('http://127.0.0.1:5000/api/send-query-rag', { query: queryToSend, user_id: this.userId }, {
  withCredentials: false // This should be explicitly set to false
})
        .then(response => {
         // const { answer, timestamp } = response.data;
          console.log(response.data);
         // const answer = response.data.choices[0].message.content; // Assuming the structure matches the OpenAI API response
          const answer= response.data['answer'];
          const docu_relevance=response.data['docu_relevance'];
          console.log(docu_relevance);
          const as_time=response.data['time_created'];
          console.log(as_time);
          console.log(response.data['total_prompt']);
        //  const timestamp = response.data.created; // The timestamp might need to be converted into a readable format
          const timestamp = new Date(as_time * 1000).toLocaleString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: true
              });
          console.log(answer); // Now log the extracted answer

          // Update chatHistory with the server's response
          this.chatHistory.push({
            sender: 'Bot',
            message: answer,
            timestamp: timestamp,
            accessedDocs:'',
            docu_rele: docu_relevance
          });
           // Save the query-answer pair along with accessed documents
          this.saveQueryAnswerPair(this.username, queryToSend, accessedDocuments, answer, timestamp);
        })
        .catch(error => {
          console.error('Error sending query:', error);
           // Optionally, handle the error by notifying the user or adding an error message to the chat history
          this.chatHistory.push({
            sender: 'Bot',
            message: 'Error retrieving response. Please try again.',
            timestamp: new Date().toISOString()
          });
          // Handle the error, possibly by notifying the user
        });
    },
    saveQueryAnswerPair(userName, query, accessedDocs, answer, timestamp) {
    axios.post('http://127.0.0.1:5000/api/save-chat-history', {
      user_name: userName,
      query_question: query,
      accessed_docs: accessedDocs,
      answer: answer,
      timestamp: timestamp
    }, {
      withCredentials: false
    })
    .then(response => {
      console.log('Chat history saved:', response.data);
    })
    .catch(error => {
      console.error('Error saving chat history:', error);
    });
  },
    clearChatHistory() {
          this.chatHistory = [];
    },
    submitFeedback() {
      const feedbackToSend = this.newFeedback;
      const username = this.username; // Ensure that userId is being set correctly

      if (!this.userId) {
        console.error('User ID is not available.');
        return; // Don't proceed without a user ID
      }

      this.newFeedback = ''; // Clear input after sending

      // Send the feedback to the server/backend
      axios.post('http://127.0.0.1:5000/api/submit-feedback', {
        feedback: feedbackToSend,
        user_name: username, // Include the user ID in the request
        fb_time: new Date().toISOString(),
      }, {
      withCredentials: false
    })
      .then(() => {
        // Feedback sent successfully
        console.log('Feedback submitted successfully');
        // Optionally clear feedback from UI or notify user of success
      })
      .catch(error => {
        console.error('Error submitting feedback:', error);
        // Handle the error, possibly by notifying the user
      });
    },

    logout() {
          // Implement logout logic here, e.g., clear session, redirect to login
        this.$router.push('/');
    }
  }
}
</script>
