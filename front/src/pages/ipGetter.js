import { useState, useEffect } from 'react';
import axios from 'axios';

/**
 * Custom hook to fetch and return the server's IPv4 address.
 */
function useIP() {
  const [ipv4, setIPv4] = useState(''); // State for the server IP address

  useEffect(() => {
    const fetchIPv4 = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get-ip'); // Fetch server IP
        setIPv4(response.data.ipv4); // Set the IP address in state
      } catch (error) {
        console.error('Failed to fetch server IP address:', error); 
      }
    };

    fetchIPv4(); // Call fetch function
  }, []);

  return ipv4; // Return the IPv4 address
}

export default useIP; 
