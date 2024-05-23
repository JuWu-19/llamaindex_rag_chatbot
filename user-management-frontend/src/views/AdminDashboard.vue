<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <p>Welcome to the Admin Dashboard!</p>

    <div class="content">
      <!-- Total Document List on the left -->
      <div class="documents">
        <h2>Total Document List</h2>
        <table>
          <thead>
            <tr>
              <th>Document Name</th>
              <th>Uploader Name</th>
              <th>Access Status</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="doc in documents" :key="doc.doc_id">
              <td>{{ doc.doc_name }}</td>
              <td>{{ doc.uploader_name }}</td>
              <td>
                <div class="access-status">
                  <span class="access-dot enabled" :class="{ active: doc.access_status === 'enabled' }" @click="setGlobalAccess(doc.doc_id, 'enabled')"></span>
                   <!-- Partial dot: Always visible but not clickable -->
                  <span class="access-dot partial" :class="{ active: doc.access_status === 'partial' }"></span>

                  <span class="access-dot disabled" :class="{ active: doc.access_status === 'disabled' }" @click="setGlobalAccess(doc.doc_id, 'disabled')"></span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

<!-- User-Specific Document Access Control on the right -->
<div class="user-access-control">
  <h2>User-Specific Document Access Control</h2>
  <select v-model="selectedUserId">
    <option v-for="user in users" :key="user.user_id" :value="user.user_id">
      {{ user.username }}
    </option>
  </select>
  <table v-if="selectedUserId">
    <thead>
      <tr>
        <th>Document Name</th>
        <th>Uploader Name</th>
        <th>Create Time</th>
        <th>Access?</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="doc in userDocuments" :key="doc.doc_id">
        <td>{{ doc.doc_name }}</td>
        <td>{{ doc.uploader_name }}</td>
        <td>{{ doc.create_time }}</td>
        <td>
          <div class="access-status">
            <!-- Access Enabled Dot -->
            <span class="access-dot enabled"
              :class="{ active: doc.has_access }"
              @click="setUserAccess(doc.doc_id, selectedUserId, true)">
            </span>

            <!-- Access Disabled Dot -->
            <span class="access-dot disabled"
              :class="{ active: !doc.has_access }"
              @click="setUserAccess(doc.doc_id, selectedUserId, false)">
            </span>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
</div>

    </div>

    <button @click="logout">Logout</button>
  </div>
</template>

<style>
.content {
  display: flex;
  justify-content: space-between;
}

.documents, .user-access-control {
  flex: 1;
  margin: 10px;
}

.access-dot.partial {
  background-color: orange;
  cursor: default; /* Change cursor to indicate non-interactivity */
  opacity: 0.5; /* Less emphasis when not active */
}

.access-dot.partial.active {
  opacity: 1; /* Full visibility when active */
}

.access-dot {
  display: inline-block;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin: 0 5px;
  cursor: pointer;
}
.access-dot.enabled { background-color: green; }

.access-dot.disabled { background-color: red; }
.access-dot.active { box-shadow: 0 0 0 2px white, 0 0 0 4px black; } /* Highlight the active status */

</style>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      documents: [], // List of all documents
      users: [], // List of users for access control
      userDocuments: [], // List of documents for the selected user
      selectedUserId: null, // Selected user ID for access control
    };
  },
  methods: {
    fetchUsers() {
    axios.get('http://127.0.0.1:5000/api/users', {
      withCredentials: false  // Ensuring credentials are not included
    })
    .then(response => {
      this.users = response.data;
      console.log("Users fetched successfully:", response.data);
      // Proceed to handle your response data
    })
    .catch(error => {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error('Error fetching users:', error.response.data);
        alert('Failed to fetch users: ' + error.response.data.message);
      } else if (error.request) {
        // The request was made but no response was received
        // `error.request` is an instance of XMLHttpRequest in the browser
        console.error('Error fetching users:', error.request);
        alert('No response received, check network or server configuration.');
      } else {
        // Something happened in setting up the request that triggered an Error
        console.error('Error fetching users:', error.message);
        alert('Error in setting up the request.');
      }
    });
  },

  fetchUserDocuments() {
  if (!this.selectedUserId) return;
  axios.get(`http://127.0.0.1:5000/user-documents/${this.selectedUserId}`, {
    withCredentials: false  // Ensuring credentials are not included
  })
  .then(response => {
    this.userDocuments = response.data;
    console.log('User documents fetched successfully:', response.data);
  })
  .catch(error => {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.error('Error fetching user documents:', error.response.data);
      console.error('Status:', error.response.status);
      console.error('Headers:', error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      console.error('User documents request was made but no response was received', error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      console.error('Error setting up request for fetching user documents:', error.message);
    }
    console.error('Config:', error.config);
  });
},
//     toggleUserAccess(docId, userId) {
//   // Assuming 'has_access' is a boolean flag that represents the current access state
//   const currentAccess = this.userDocuments.find(doc => doc.doc_id === docId).has_access;
  
//   axios.post('http://127.0.0.1:5000/user-documents/access', {
//     user_id: userId,
//     doc_id: docId,
//     access_right: !currentAccess  // Toggle the current access right
//   }, {
//       withCredentials: false  // Ensuring credentials are not included
//     })
//   .then(() => {
//     this.fetchUserDocuments(userId); // Refresh the list to show the updated access rights
//     this.refreshAccessStatus(); // Optionally refresh global document status if needed
//   })
//   .catch(error => {
//     console.error('Error toggling user document access:', error);
//     alert('Failed to update document access.');
//   });
// },
setGlobalAccess(docId, status) {
  axios.post('http://127.0.0.1:5000/documents/set-access', { doc_id: docId, status: status }, {
      withCredentials: false  // Ensuring credentials are not included
    })
    .then(() => {
      this.refreshAccessStatus();
      if (this.selectedUserId) {
      this.fetchUserDocuments(this.selectedUserId); // Refresh user-specific documents if a user is selected
    }
      if (status === 'enabled') {
        alert('Document access enabled for all users');
      } else {
        alert('Document access disabled for all users');
      }
    })
    .catch(error => {
      console.error('Error setting global access:', error);
    });
},
setUserAccess(docId, userId, access) {
    axios.post('http://127.0.0.1:5000/user-documents/access', {
      user_id: userId,
      doc_id: docId,
      access_right: access
    }, {
      withCredentials: false
    })
    .then(() => {
      this.fetchUserDocuments(this.selectedUserId); // Refresh the list to show the updated access rights
      this.refreshAccessStatus(); // Refresh global document status to reflect changes immediately
    })
    .catch(error => {
      console.error('Error setting user document access:', error);
      alert('Failed to update document access.');
    });
  },
refreshAccessStatus() {
    axios.get('http://127.0.0.1:5000/documents/access/refresh', {
      withCredentials: false  // Ensuring credentials are not included
    })
    .then(response => {
      this.documents = response.data;
      console.log("Access status refreshed:", response.data);
      // Update the state or react to the data as necessary
    })
    .catch(error => {
      if (error.response) {
        console.error('Error refreshing access status:', error.response.data);
        alert('Failed to refresh access status: ' + error.response.data.message);
      } else {
        console.error('Network Error or CORS issue', error);
        alert('A network error occurred or CORS is misconfigured');
      }
    });
  },
logout() {
  // Implement logout logic here, for example by clearing user session
  this.$router.push('/'); // Redirect to the home or login page after logout
}
},
  created() {
    this.fetchUsers();
    this.refreshAccessStatus();
  },
  watch: {
    selectedUserId(newVal) {
      if (newVal) {
        this.fetchUserDocuments(newVal);
      }
    }
  }
}
</script>
