function CheckEmailPage() {
    return (
        <div className="max-w-xl mx-auto mt-10 p-6 bg-white rounded shadow">
            <h2 className="text-2xl font-bold mb-4">Almost there!</h2>
            <p className="text-gray-700">
                Please check your inbox. We've sent you an email with a link to verify your account.
            </p>
            <p className="text-sm text-gray-500 mt-2">
                Didn’t get the email? Check your spam folder or try registering again.
            </p>
        </div>
    );
}

export default CheckEmailPage;
