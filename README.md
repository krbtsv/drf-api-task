# Test task for Emphasoft - DRF api

## Functional
+ Create User
+ Authentication user from token
+ Create books
+ Users can execute CRUD(the books) according to permissions

Read data - access for everyone  
Create data - access for authorized users  
Update data - access for creator  
Delete data - access for creator  

admin - full access
___
### For Linux
___
#### Clone repository

    git clone https://github.com/krbtsv/drf_api_task.git
    cd drf_api_task

#### Deploying

    chmod +x ./deploy    
    ./deploy

#### Starting the development server

    cd backend
    chmod +x ./bin/run
    ./bin/run
