import { describe, expect, it } from "vitest";
import { validateEmail, validatePassword } from "./authValidation";

describe("validateEmail", () => {
  it("returns an error for empty input", () => {
    expect(validateEmail("")).toMatch(/required/i);
    expect(validateEmail(null)).toMatch(/required/i);
  });

  it("returns an error for malformed addresses", () => {
    expect(validateEmail("not-an-email")).toMatch(/valid/i);
    expect(validateEmail("a@b")).toMatch(/valid/i);
    expect(validateEmail("a @b.com")).toMatch(/valid/i);
  });

  it("returns null for plausible addresses", () => {
    expect(validateEmail("user@example.com")).toBeNull();
    expect(validateEmail(" user@example.com ")).toBeNull();
  });
});

describe("validatePassword", () => {
  it("returns an error for empty input regardless of mode", () => {
    expect(validatePassword("", "register")).toMatch(/required/i);
    expect(validatePassword("", "login")).toMatch(/required/i);
  });

  it("login mode skips complexity checks", () => {
    expect(validatePassword("short", "login")).toBeNull();
    expect(validatePassword("nodigits", "login")).toBeNull();
  });

  it("register mode requires 8+ chars", () => {
    expect(validatePassword("short1", "register")).toMatch(/8/);
  });

  it("register mode requires a letter", () => {
    expect(validatePassword("12345678", "register")).toMatch(/letter/i);
  });

  it("register mode requires a number", () => {
    expect(validatePassword("alphabetonly", "register")).toMatch(/number/i);
  });

  it("register mode passes with letter + number + 8 chars", () => {
    expect(validatePassword("password1", "register")).toBeNull();
  });
});
