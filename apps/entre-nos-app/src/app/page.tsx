import './style.css'

export default function Home() {
  return (
    <div className='corpo'>
      <div className="container">
        <div className="form_area">
          <p className="title">ENTRAR</p>
          <form action="">
            <div className="form_group">
              <label className="sub_title" htmlFor="email">Email</label>
              <input placeholder="Enter your email" id="email" className="form_style" type="email" />
            </div>
            <div className="form_group">
              <label className="sub_title" htmlFor="password">Password</label>
              <input placeholder="Enter your password" id="password" className="form_style" type="password" />
            </div>
            <div>
              <button className="btn">ENTRAR</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
