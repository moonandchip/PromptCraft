import { createContext, useContext, useState } from "react";
import styles from "./LoadingContext.module.css";

const LoadingContext = createContext();

// Helper function to let api.js toggle loading globally
let setGlobalLoadingInternal = null;
export function setGlobalLoading(state) {
  if (setGlobalLoadingInternal) setGlobalLoadingInternal(state);
}

export function LoadingProvider({ children }) {
  const [loading, setLoading] = useState(false);

  // Expose setter to api.js
  setGlobalLoadingInternal = setLoading;

  return (
    <LoadingContext.Provider value={{ loading }}>
      {children}
      {loading && (
        <div className={styles.loaderOverlay}>
          <div className={styles.spinner}></div>
        </div>
      )}
    </LoadingContext.Provider>
  );
}

export function useLoading() {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error("useLoading must be used within a LoadingProvider");
  }
  return context;
}
