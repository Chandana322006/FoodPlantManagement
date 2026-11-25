
flowchart LR
    Admin([Admin])
    Staff([Production Staff])
    Quality([Quality Manager])
    Supervisor([Supervisor])
    Manager([Management])

    subgraph App["Food Plant Operations Management App"]
        Login[Login]
        Users[Manage Users and Roles]
        Master[Manage Master Data]
        Production[Enter Production Records]
        QualityTest[Enter Quality Test Results]
        Import[Import Historical Data]
        Approve[Review and Approve Records]
        Reports[View Production Reports]
        Export[Export CSV and PDF]
        Audit[View Audit Trail]
    end

    Admin --> Login
    Staff --> Login
    Quality --> Login
    Supervisor --> Login
    Manager --> Login

    Admin --> Users
    Admin --> Master
    Admin --> Import
    Staff --> Production
    Quality --> QualityTest
    Supervisor --> Approve
    Supervisor --> Reports
    Manager --> Reports
    Manager --> Export
    Admin --> Audit
    Supervisor --> Audit
