import React from 'react'
import { Link } from 'react-router-dom';

//purely functional no state
export default function Header() {
    return (
        <header style={headerStyle}>
            <h1>Seekr: All Lost Items</h1>
            <Link style={linkStyle} to="/">Add</Link> |
            <Link style={linkStyle} to="/search"> Search</Link> |
            <Link style={linkStyle} to="/about"> About</Link>
        </header>
    )
}

const linkStyle = {
    color: '#fff',
    textDecoration: 'none'
}

const headerStyle = {
    background: '#333',
    color: '#fff',
    textAlign: 'center',
    padding: '10px'
}
