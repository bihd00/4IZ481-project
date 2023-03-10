import { initializeApp } from "firebase/app";
import { toast } from "../stores/toast";
import { modal } from "../stores/modal";
import { ulid } from "ulid";
import { generator, preview, type Image } from "../stores/generator";
import {
  createUserWithEmailAndPassword,
  type UserCredential,
} from "firebase/auth";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  signOut as signOutFB,
  signInWithEmailAndPassword as loginWithEmailAndPassword,
} from "firebase/auth";
import config from "../firebase-config";

// init
const app = initializeApp(config);

// auth
export const auth = getAuth(app);

export async function signUpWithEmailAndPassword(
  email: string,
  password: string
) {
  const credential = createUserWithEmailAndPassword(auth, email, password);
  return loginHandler(credential);
}

export async function signInWithGoogle() {
  const credential = signInWithPopup(auth, new GoogleAuthProvider());
  return loginHandler(credential);
}

export async function signInWithEmailAndPassword(
  email: string,
  password: string
) {
  const credential = loginWithEmailAndPassword(auth, email, password);
  return loginHandler(credential);
}

async function loginHandler(promise: Promise<UserCredential>) {
  let res: any, serverError: string;
  try {
    res = await promise;
    modal.set(null);
    toast.set({
      message: "Access granted!",
      type: "success",
    });
  } catch (err) {
    serverError = err.message;
    console.error(err);
    toast.set({
      message: serverError,
      type: "error",
    });
  }
  return { res, serverError };
}

export async function signOut() {
  await signOutFB(auth);
  toast.set({
    icon: "👋",
    message: "Thanks for hanging out, see ya around!",
  });
}

// generator
export async function generateImages(text: string) {
  const { getFirestore, collection, addDoc, query, where, onSnapshot } =
    await import("firebase/firestore");
  let res: any, serverError: string;

  const firestore = getFirestore();
  const refId = ulid();
  const currentDt = new Date().toISOString();
  const q = query(collection(firestore, "images"), where("refId", "==", refId));

  const newText = { refId, content: text, createdAt: currentDt };
  let unsubImages: () => void;

  try {
    await addDoc(collection(firestore, "texts"), newText);
    generator.set({ refId, text: newText });
    unsubImages = onSnapshot(q, (snap) => {
      const images: Image[] = [];
      snap.forEach((doc) => images.push(doc.data() as Image));
      generator.update((g) => ({ ...g, images }));
    });

    if (auth.currentUser) {
      await addDoc(collection(firestore, "refs"), {
        uid: auth.currentUser.uid,
        refId,
        createdAt: currentDt,
      });
    }
  } catch (e) {
    toast.set({
      message: `Error adding document: ${e}`,
      type: "error",
    });
    serverError = e.message;
  }

  return { res, serverError, unsubImages };
}

export async function getPreviewImages() {
  const { getFirestore, collection, query, limit, orderBy, getDocs } =
    await import("firebase/firestore");
  let res: any, serverError: string;

  const firestore = getFirestore();
  const previewImagesQuery = query(
    collection(firestore, "images"),
    orderBy("createdAt", "desc"),
    limit(10)
  );

  const images: Image[] = [];
  try {
    const docRefs = await getDocs(previewImagesQuery);
    docRefs.forEach((doc) => images.push(doc.data() as Image));
    res = images;
    preview.set({ images });
  } catch (err) {
    serverError = err.message;
  }

  return { res, serverError };
}
