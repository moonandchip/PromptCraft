import { Component } from "react";

export default class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { error: null };
  }

  static getDerivedStateFromError(error) {
    return { error };
  }

  componentDidCatch(error, info) {
    console.error("Unhandled render error:", error, info);
  }

  handleReload = () => {
    this.setState({ error: null });
    window.location.assign("/");
  };

  render() {
    if (this.state.error) {
      return (
        <div
          style={{
            maxWidth: 480,
            margin: "10vh auto",
            padding: "32px 24px",
            textAlign: "center",
            fontFamily: "ui-sans-serif, system-ui, sans-serif",
            color: "#1f2937",
          }}
        >
          <h1 style={{ fontSize: 24, marginBottom: 12 }}>Something went wrong.</h1>
          <p style={{ color: "#6b7280", marginBottom: 24 }}>
            The page hit an unexpected error. Refresh to try again.
          </p>
          <button
            type="button"
            onClick={this.handleReload}
            style={{
              padding: "10px 18px",
              background: "#2563eb",
              color: "#fff",
              border: "none",
              borderRadius: 8,
              fontWeight: 500,
              cursor: "pointer",
            }}
          >
            Back to home
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
