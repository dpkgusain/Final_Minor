import React from "react";
import {
  FaFacebookF,
  FaInstagram,
  FaTwitter,
  FaLinkedin,
  FaGithub,
} from "react-icons/fa";

import ContentWrapper from "../contentWrapper/ContentWrapper";

import "./style.scss";

const Footer = () => {
  return (
    <footer className="footer">
      <ContentWrapper>
        <ul className="menuItems">
          <li className="menuItem">Terms Of Use</li>
          <li className="menuItem">Privacy-Policy</li>
          <li className="menuItem">About</li>
          <li className="menuItem">Blog</li>
          <li className="menuItem">FAQ</li>
        </ul>
        <div className="infoText">
          © 2024 Chillax - Max Relax, Zero Drax. Where Entertainment Meets
          Connection. Bringing movies, series, and music together for a
          personalized, socially connected experience. Enjoy, explore, and
          share—anytime, anywhere.
        </div>
        <div className="socialIcons">
          <span className="icon">
            <FaFacebookF />
          </span>
          <span className="icon">
            <a href="" target="_blank">
              <FaInstagram />
            </a>
          </span>
          <span className="icon">
            <a href="https://github.com/dpkgusain/Final_Minor" target="_blank">
              {" "}
              <FaGithub />
            </a>
          </span>
          <span className="icon">
            <a
              href="https://www.linkedin.com/in/manya-0a9314256/"
              target="_blank"
            >
              {" "}
              <FaLinkedin />
            </a>
          </span>
        </div>
      </ContentWrapper>
    </footer>
  );
};

export default Footer;
