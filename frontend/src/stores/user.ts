import { writable } from "svelte/store";
import { auth } from "../services/firebase";
import { onAuthStateChanged } from "firebase/auth";
import type { User } from "firebase/auth";
import type { Image, Ref } from "./generator";

export interface UserData {
  uid?: string;
  images?: Image[];
}

export const user = writable<User>(null);
export const userData = writable<UserData>(null);

let unsubData: () => void;

onAuthStateChanged(auth, async (appUser) => {
  user.set(appUser);
  if (appUser) {
    const {
      getFirestore,
      collection,
      getDocs,
      query,
      where,
      orderBy,
      onSnapshot,
      limit,
    } = await import("firebase/firestore");

    const firestore = getFirestore();

    const uid = appUser.uid;
    const userRefsQuery = query(
      collection(firestore, "refs"),
      where("uid", "==", uid),
      orderBy("createdAt", "desc"),
      limit(8)
    );

    unsubData = onSnapshot(userRefsQuery, async (snap) => {
      const refs: Ref[] = [];
      snap.forEach((doc) => refs.push(doc.data() as Ref));
      const refIds = refs.slice(0, 9).map((ref) => ref.refId);

      const userImagesQuery = query(
        collection(firestore, "images"),
        where("refId", "in", refIds),
        orderBy("createdAt", "desc"),
        limit(8)
      );

      const images: Image[] = [];
      const imageRefs = await getDocs(userImagesQuery);
      imageRefs.forEach((doc) => images.push(doc.data() as Image));

      userData.set({ uid, images });
    });
  } else {
    unsubData && unsubData();
    userData.set(null);
  }
});
