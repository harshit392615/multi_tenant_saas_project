import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("../serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# // Import the functions you need from the SDKs you need
# import { initializeApp } from "firebase/app";
# import { getAnalytics } from "firebase/analytics";
# // TODO: Add SDKs for Firebase products that you want to use
# // https://firebase.google.com/docs/web/setup#available-libraries

# // Your web app's Firebase configuration
# // For Firebase JS SDK v7.20.0 and later, measurementId is optional
# const firebaseConfig = {
#   apiKey: "AIzaSyBYxIJwowWh1fjYRtPapy-6LcmzBMDvFIA",
#   authDomain: "mtsp-90f54.firebaseapp.com",
#   projectId: "mtsp-90f54",
#   storageBucket: "mtsp-90f54.firebasestorage.app",
#   messagingSenderId: "117372393169",
#   appId: "1:117372393169:web:62d31a758de186d20197f0",
#   measurementId: "G-8JX78LCYSJ"
# };

# // Initialize Firebase
# const app = initializeApp(firebaseConfig);
# const analytics = getAnalytics(app);