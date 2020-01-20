void main()
{
    A();
    B();
    for(int i = 0; i < 2; ++i)
    {
        if(i % 2)
            C();
        else
            D();
    }
}
