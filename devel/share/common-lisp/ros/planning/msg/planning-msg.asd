
(cl:in-package :asdf)

(defsystem "planning-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ChouChou" :depends-on ("_package_ChouChou"))
    (:file "_package_ChouChou" :depends-on ("_package"))
  ))