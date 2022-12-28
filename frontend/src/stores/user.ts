import { writable } from "svelte/store";
import { auth } from "../services/firebase";
import { onAuthStateChanged } from "firebase/auth";
import type { User } from "firebase/auth";

export interface UserData {
  email?: string;
  uid?: string;
  displayName?: string;
  photoURL?: string;
  joined?: number;
  stripeCustomerId?: string;
  discordId?: string;
  is_pro?: boolean;
  expires?: number;
  enterprise?: boolean;
  enterpriseOwner?: string;
  pro_status?:
    | "lifetime"
    | "active"
    | "past_due"
    | "expiring"
    | "canceled"
    | "enterprise";
  subscriptions?: {
    [key: string]: string;
  };
  sentMail?: {
    [key: string]: boolean;
  };
}

export const user = writable<User>(null);
export const userData = writable<UserData>(null);

let unsubData: () => void;

onAuthStateChanged(auth, async (appUser) => {
  user.set(appUser);
  if (appUser) {
    const { doc, onSnapshot, getFirestore } = await import(
      "firebase/firestore"
    );
    const firestore = getFirestore();
    const userRef = doc(firestore, `users/${appUser.uid}`);
    unsubData = onSnapshot(userRef, (snap) => {
      userData.set(snap.data() as UserData);
    });
  } else {
    unsubData && unsubData();
    userData.set(null);
  }
});
