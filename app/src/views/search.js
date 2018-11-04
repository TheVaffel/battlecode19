import React, { Component } from 'react';
import Api from '../api';

class PaginatedList extends Component {
    renderPagination = () => {
        const { props } = this;

        if (!props.pageLimit || props.pageLimit<= 1) { 
            return null;
        };

        const items = [];
        const isFirst = props.page === 1;
        const isLast = props.page === props.pageLimit;

        items.push(
            <li className={isFirst ? "page-item disabled" : "page-item"} key="prev">
                <a className="page-link" onClick={() => props.onPageClick(props.page - 1)}>Previous</a>
            </li>
        );


        for (let i = 1; i <= props.pageLimit; i++) {
            items.push(
                <li className = {i === props.page ? "page-item active" : "page-item"} key={i}>
                    <a className="page-link" onClick = {() => props.onPageClick(i)}>{i}</a>
                </li>
            )
        }

        items.push(
            <li className={isLast ? "page-item disabled" : "page-item"} key="next">
                <a className="page-link" onClick={() => props.onPageClick(props.page + 1)}>Next</a>
            </li>
        );

        return (
            <ul className="pagination"> 
                {items}
            </ul>
        )
    }
}

class UserList extends PaginatedList {

    render() {
        const { props } = this;

        if (props.users.length === 0) {
            return null;
        }
        
        return (
            <div>
                <div className="card">
                    <div className="header">
                        <h4 className="title">Users</h4>
                    </div>
                    <div className="content table-responsive table-full-width">
                        <table className="table table-hover table-striped">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Country</th>
                                <th>Bio</th>
                            </tr>
                        </thead>
                            <tbody>
                                { props.users.map(user => 
                                        <tr key={ user.username }>
                                        <td>{ user.username }</td>
                                        <td>{ user.country }</td>
                                        <td>{ user.bio }</td>
                                        </tr> 
                                    )
                                }
                            </tbody>
                        </table>
                    </div>
                </div>
                {this.renderPagination()}
            </div>
        );
    }
}

class TeamList extends PaginatedList {

    render() {
        if (this.props.teams.length > 0) return (
            <div>
                <div className="card">
                    <div className="header">
                        <h4 className="title">Teams</h4>
                    </div>
                    <div className="content table-responsive table-full-width">
                        <table className="table table-hover table-striped">
                            <thead>
                            <tr>
                                <th>Team</th>
                                <th>Users</th>
                                <th>Bio</th>
                            </tr>
                            </thead>
                            <tbody>
                                { 
                                    this.props.teams.map(team => 
                                        <tr key={ team.id }>
                                        <td>{ team.name }</td>
                                        <td>{ team.users.join(", ") }</td>
                                        <td>{ team.bio }</td>
                                        </tr> )
                                }
                            </tbody>
                        </table>
                    </div>
                </div>
                {this.renderPagination()}
            </div>
        );
        else return (<div></div>);
    }
}


class Search extends Component {

    state = {
        users:[],
        userLimit: 0,
        userPage: 1,
        teams:[],
        teamLimit: 0,
        teamPage: 1,
        input: "",
    };    
    
    componentDidMount() {
        Api.search(this.state.input, this.onDataLoad);
    }

    handleChange = (e) => {
        this.setState({ input: e.target.value });
    } 

    onDataLoad = (data) => {
        this.setState(data);
    }

    getTeamPage = (page) => {
        const { state } = this;
        if (page !== state.teamPage && page >= 0 && page <= state.teamLimit) {
            Api.searchTeam(state.input, page, this.onDataLoad);
        }
    }

    getUserPage = (page) => {
        const { state } = this;
        if (page !== state.userPage && page >= 0 && page <= state.userLimit) {
            Api.searchUser(state.input, page, this.onDataLoad);
        }
    }

    search = (e) => {
        e.preventDefault();
        Api.search(this.state.input, this.onDataLoad);
    }

    render() {
        const { state } = this;
        return (
            <div className="content">
                <div className="container-fluid row">
                    <div className="col-md-12">
                        <div className="card">
                            <div className="content">
                                <form className="input-group" onSubmit={this.search}>
                                    <input type="text" className="form-control" onChange={this.handleChange} placeholder="Search for..." />
                                    <span className="input-group-btn">
                                        <button className="btn btn-default" type='submit' value="Submit">Go!</button>
                                    </span>
                                </form>
                            </div>
                        </div>
                    </div>
                    <div className="col-md-12">
                        <UserList 
                            users = {state.users} 
                            page = {state.userPage}
                            pageLimit = {state.userLimit}
                            onPageClick = {this.getUserPage}
                        />
                    </div>
                    <div className="col-md-12">
                        <TeamList 
                            teams={state.teams}
                            page = {state.teamPage}
                            pageLimit = {state.teamLimit}
                            onPageClick = {this.getTeamPage}
                        />
                    </div>
                </div>
            </div>
        );
    }
}

export default Search;