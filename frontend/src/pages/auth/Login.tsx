import React from "react";
import { Button, Alert, Row, Col } from "react-bootstrap";
import { Navigate, Link, useLocation } from "react-router-dom";
import { useTranslation } from "react-i18next";
import * as yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import classNames from "classnames";
import axios from "axios";
import Cookies from "js-cookie";

// components
import { VerticalForm, FormInput } from "../../components/";
import AuthLayout from "./AuthLayout";

const API_BASE_URL = "http://localhost:8000/server_api";

/* bottom links */
const BottomLink = () => {
  const { t } = useTranslation();

  return (
    <Row className="mt-3">
      <Col className="text-center">
        <p>
          <Link to={"/auth/forget-password"} className="text-white-50 ms-1">
            {t("Forgot your password?")}
          </Link>
        </p>
        <p className="text-white-50">
          {t("Don't have an account?")}{" "}
          <Link to={"/auth/register"} className="text-white ms-1">
            <b>{t("Sign Up")}</b>
          </Link>
        </p>
      </Col>
    </Row>
  );
};

/* social links */
const SocialLinks = () => {
  const socialLinks = [
    {
      variant: "primary",
      icon: "facebook",
    },
    {
      variant: "danger",
      icon: "google",
    },
    {
      variant: "info",
      icon: "twitter",
    },
    {
      variant: "secondary",
      icon: "github",
    },
  ];
  return (
    <ul className="social-list list-inline mt-3 mb-0">
      {(socialLinks || []).map((item, index: number) => {
        return (
          <li key={index} className="list-inline-item">
            <Link
              to="#"
              className={classNames(
                "social-list-item",
                "border-" + item.variant,
                "text-" + item.variant
              )}
            >
              <i className={classNames("mdi", "mdi-" + item.icon)}></i>
            </Link>
          </li>
        );
      })}
    </ul>
  );
};

const Login = () => {
  const { t } = useTranslation();
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const [username, setUserName] = React.useState("");
  const [password, setPassword] = React.useState("");

  const user = Cookies.get("user");

  const location = useLocation();
  const redirectUrl = location?.search?.slice(6) || "/";

  if (user) {
    return <Navigate to={redirectUrl} />;
  }

  /*
  form validation schema
  */
  const schemaResolver = yupResolver(
    yup.object().shape({
      username: yup.string().required(t("Please enter Username")),
      password: yup.string().required(t("Please enter Password")),
    })
  );

  /*
  handle form submission
  */
  const onSubmit = async () => {
    setLoading(true);
    try {
      console.log("Form Data:", username);
      console.log("Form password:", password);
      // Make API request to login
      const response = await axios.post(`${API_BASE_URL}/business-admin/login/`, {
        username,
        password
      });

      // Log the response to inspect its structure
      console.log("API Response:", response);

      if (response && response.data && response.data.message === "Logged In") {
        Cookies.set("user", JSON.stringify(response.data.user));
        window.location.href = redirectUrl;
      } else {
        setError("Unexpected response structure.");
      }
    } catch (e) {
      console.error("Error occurred:", e); // Log the error for more details
      setError((e as any).message || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout
      helpText={t(
        "Enter your email address and password to access admin panel."
      )}
      bottomLinks={<BottomLink />}
    >
      {error && (
        <Alert variant="danger" className="my-2">
          {error}
        </Alert>
      )}

      <VerticalForm onSubmit={onSubmit} resolver={schemaResolver}>
        <FormInput
          label={t("Username")}
          type="text"
          name="username"
          placeholder="Enter your Username"
          onChange={(e) => setUserName(e.target.value)}
          containerClass={"mb-3"}
        />
        <FormInput
          label={t("Password")}
          type="text"
          name="password"
          placeholder="Enter your password"
          onChange={(e) => setPassword(e.target.value)}
          containerClass={"mb-3"}
        />

        <div className="text-center d-grid">
          <Button variant="primary" type="submit" disabled={loading}>
            {t("Log In")}
          </Button>
        </div>
      </VerticalForm>

      <div className="text-center">
        <h5 className="mt-3 text-muted">{t("Sign in with")}</h5>
        <SocialLinks />
      </div>
    </AuthLayout>
  );
};

export default Login;
