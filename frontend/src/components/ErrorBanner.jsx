import styles from "./ErrorBanner.module.css";

/**
 * Reusable error banner component for displaying API or UI errors.
 * @param {Object} props
 * @param {string} props.message - Error message to display
 * @param {function} [props.onClose] - Optional callback to dismiss the error
 */
export default function ErrorBanner({ message, onClose }) {
  if (!message) return null;

  return (
    <div className={styles.container}>
      <span className={styles.text}>❌ {message}</span>
      {onClose && (
        <button onClick={onClose} className={styles.closeButton}>
          ✖
        </button>
      )}
    </div>
  );
}
